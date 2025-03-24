artists = ["Hans Zimmer", "Danny Elfman", "The Police", "Call the Police", "James Newton Howard"]
select_artist = [artist for artist in artists if "police" in artist.lower()]
print(select_artist)

composers = ["Hans Zimmer", "Danny Elfman", "James Newton Howard", "Randy Newman", "Howard Shore"]
select_composers = [composer.upper() for composer in composers if "Howard" in composer]
print(select_composers)