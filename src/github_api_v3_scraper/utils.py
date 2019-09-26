import links_from_header


def get_next(headers):
    links_header = headers.get("Link", None)
    if links_header:
        links = links_from_header.extract(links_header.decode())
        if "next" in links:
            return links["next"]
    return None
