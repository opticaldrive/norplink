domains = open("domains.txt", "r").readlines()
domains = [domain.strip().lower() for domain in domains]
domain_total = len(domains) 
print(domains)

