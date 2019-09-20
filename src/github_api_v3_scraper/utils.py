def get_next(headers):
    header_links = headers.get("Link", None)
    if header_links:
        links = header_links.split(",")
        for link in links:
            if 'rel="next"' in link:
                l, rel = link.split(";")
                l = l.lstrip("<")
                l = l.rstrip(">")
                return l
    return None
