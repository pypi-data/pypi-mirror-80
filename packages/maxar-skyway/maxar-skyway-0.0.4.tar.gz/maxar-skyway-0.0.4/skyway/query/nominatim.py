import typing
from collections import defaultdict
import collections.abc
import functools
import csv

from .filters import TagFilter, format_values
from .query import element_query_factory, reduce_union_or


def parse_feature_description(desc):
    tagmap = defaultdict(list)
    s = [_.strip().split("=") for _ in desc.split("OR")]
    for k, v in s:
        tagmap[k].append(v)
    return tagmap

def parse_feature_elements(elms, delim="_"):
    return [int(lev) for lev in elms.split(delim)]


def nominatim_from_csv(path):
    # handle in-memory file handle (e.g. instances of io.BytesIO)
    if isinstance(path, str):
        path = open(path)

    reader = csv.DictReader(path)
    d = defaultdict(list)
    for row in reader:
        d[row['FeatureName']].append(row['TagFilterDescription'])
        if 'Elements' in row:
            elements = [int(num) for num in row["Elements"].split('_')]
            d[row['FeatureName']].append(elements)

    # close file
    path.close()
    return d


class PrimaryFeature(typing.NamedTuple):
    name: str
    source_desc: str
    elements: collections.abc.Sequence = [1, 2, 3]

    @property
    def ElementQuery(self):
        if isinstance(self.elements, str):
            self.elements = parse_feature_elements(self.elements)

        return element_query_factory(self.elements)

    @property
    def tag_profile(self):
        return dict(parse_feature_description(self.source_desc))

    def compile_QL(self, *args, **kwargs):
        wildkeys, tagkeys = [], []
        tagmap = self.tag_profile
        while tagmap:
            k, v = tagmap.popitem()
            if v == ['*']:
                wildkeys.append(k)
            else:
                tagkeys.append(TagFilter(k, vals=v))

        # format wildcard keys if exist
        tfs = []
        if wildkeys:
            if len(wildkeys) == 1:
                fargs = wildkeys.pop()
            else:
                fargs = format_values(wildkeys)
            tfs.append(TagFilter(fargs))
        tfs.extend(tagkeys)
        qs = [self.ElementQuery(filters=tf) for tf in tfs]
        return reduce_union_or(qs)


class Nominatim:
    def __init__(self, d):
        self.feature_map = {feature_name.replace("-", "_"): PrimaryFeature(feature_name, description, elements) for feature_name, (description, elements) in d.items()}

    def desc(self):
        for name, feature in self.feature_map.items():
            print(f"{name}: {feature.compile_QL()}")

    def _map_profiles_by_eqtype(self, *args):
        feature_names = args or self.feature_map.keys()
        result = defaultdict(lambda: defaultdict(list))
        for name in feature_names:
            feature = self.feature_map[name]
            element_tags = result[feature.ElementQuery]
            for tag_key, tag_list in feature.tag_profile.items():
                element_tags[tag_key].extend(tag_list)

        return result

    def _consolidate_element_queries(self, *args):
        md = self._map_profiles_by_eqtype(*args)
        query_list = []
        for EQ, tpfs in md.items():
            tag_filters = [TagFilter(k, vals=vals) for k, vals in tpfs.items()]
            element_queries = [EQ(filters=tag_filter) for tag_filter in tag_filters]
            unioned_query = reduce_union_or(element_queries)
            query_list.append(unioned_query)

        return query_list

    def compress_feature_queries(self, *args):
        """
        Takes a number of feature names, groups their tag profiles by
        element query type and then by tag-key, then builds and unionizes the
        resulting queries element queries, potentially reducing the number of
        unions resulting from combining features with shared elements and tag-
        profile keys. This can result in more effcient queries than simply adding
        feature queries together, since it reduces IO by eliminating redundancy
        incurred via shared tag profiles and query types.

        If no arguments are passed, this function builds the compressed QL for the
        entire collection of the features defined on it.
        """

        qlist = self._consolidate_element_queries(*args)
        return reduce_union_or(qlist)

    @classmethod
    def from_csv(cls, path):
        d = nominatim_from_csv(path)
        return cls(d)
