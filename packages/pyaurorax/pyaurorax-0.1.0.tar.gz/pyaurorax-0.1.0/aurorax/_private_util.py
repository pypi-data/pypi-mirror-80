def set_url(part1: str, part2: str) -> str:
    """
    Create URL using the latest URL_API_STUB value

    :param part1: part 1 to stitch together
    :type part1: str
    :param part2: part 2 to stitch together
    :type part2: str

    :return: stitched url string
    :rtype: str
    """
    return "%s/%s" % (part1, part2)
