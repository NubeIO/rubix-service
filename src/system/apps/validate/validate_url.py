def validate_url(url, app_domain) -> bool:
    u = url.split("/")
    domain = (u[2], u[4], u[5])
    print("URL check:", domain, app_domain)
    return app_domain == domain
