#!/usr/bin/env python3

import json
import time
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configuracao de Log
LOG_FILE = "/home/ednitro/projetoPessoal/python/gerarJSONComListaFilmesComUrlImagem/logs/generate_movies_json.log"

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# =============================================================================
# TMDB CONFIGURATION
# =============================================================================
TMDB_API_KEY = "XXX"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
# Pode alterar para "original" se desejar imagens em resolucao maxima
TMDB_IMAGE_SIZE = "w1280"

MOVIES = [
    {"name": "Mad Max: Estrada da Furia", "name_en": "Mad Max: Fury Road", "year": 2015, "director": "George Miller", "category": "Acao", "slug": "mad-max-fury-road-2015"},
    {"name": "Duro de Matar", "name_en": "Die Hard", "year": 1988, "director": "John McTiernan", "category": "Acao", "slug": "die-hard-1988"},
    {"name": "John Wick: De Volta ao Jogo", "name_en": "John Wick", "year": 2014, "director": "Chad Stahelski", "category": "Acao", "slug": "john-wick-2014"},
    {"name": "O Exterminador do Futuro 2: O Julgamento Final", "name_en": "Terminator 2: Judgment Day", "year": 1991, "director": "James Cameron", "category": "Acao", "slug": "terminator-2-judgment-day-1991"},
    {"name": "Missao: Impossivel - Efeito Fallout", "name_en": "Mission: Impossible - Fallout", "year": 2018, "director": "Christopher McQuarrie", "category": "Acao", "slug": "mission-impossible-fallout-2018"},
    {"name": "Matrix", "name_en": "The Matrix", "year": 1999, "director": "Lana e Lilly Wachowski", "category": "Acao", "slug": "the-matrix-1999"},
    {"name": "Batman: O Cavaleiro das Trevas", "name_en": "The Dark Knight", "year": 2008, "director": "Christopher Nolan", "category": "Acao", "slug": "the-dark-knight-2008"},
    {"name": "Aliens, O Resgate", "name_en": "Aliens", "year": 1986, "director": "James Cameron", "category": "Acao", "slug": "aliens-1986"},
    {"name": "O Resgate do Soldado Ryan", "name_en": "Saving Private Ryan", "year": 1998, "director": "Steven Spielberg", "category": "Acao", "slug": "saving-private-ryan-1998"},
    {"name": "Gladiador", "name_en": "Gladiator", "year": 2000, "director": "Ridley Scott", "category": "Acao", "slug": "gladiator-2000"},
    {"name": "Os Cacadores da Arca Perdida", "name_en": "Raiders of the Lost Ark", "year": 1981, "director": "Steven Spielberg", "category": "Acao", "slug": "raiders-of-the-lost-ark-1981"},
    {"name": "Top Gun: Maverick", "name_en": "Top Gun: Maverick", "year": 2022, "director": "Joseph Kosinski", "category": "Acao", "slug": "top-gun-maverick-2022"},
    {"name": "Kill Bill: Volume 1", "name_en": "Kill Bill: Vol. 1", "year": 2003, "director": "Quentin Tarantino", "category": "Acao", "slug": "kill-bill-vol-1-2003"},
    {"name": "Busca Implacavel", "name_en": "Taken", "year": 2008, "director": "Pierre Morel", "category": "Acao", "slug": "taken-2008"},
    {"name": "Velozes e Furiosos 5: Operacao Rio", "name_en": "Fast Five", "year": 2011, "director": "Justin Lin", "category": "Acao", "slug": "fast-five-2011"},
    {"name": "Logan", "name_en": "Logan", "year": 2017, "director": "James Mangold", "category": "Acao", "slug": "logan-2017"},
    {"name": "O Profissional", "name_en": "Leon: The Professional", "year": 1994, "director": "Luc Besson", "category": "Acao", "slug": "leon-the-professional-1994"},
    {"name": "Identidade Bourne", "name_en": "The Bourne Identity", "year": 2002, "director": "Doug Liman", "category": "Acao", "slug": "the-bourne-identity-2002"},
    {"name": "Operacao Invasao", "name_en": "The Raid", "year": 2011, "director": "Gareth Evans", "category": "Acao", "slug": "the-raid-2011"},
    {"name": "Tropa de Elite", "name_en": "Elite Squad", "year": 2007, "director": "Jose Padilha", "category": "Acao", "slug": "elite-squad-2007"},
    {"name": "Vingadores: Ultimato", "name_en": "Avengers: Endgame", "year": 2019, "director": "Anthony e Joe Russo", "category": "Acao", "slug": "avengers-endgame-2019"},
    {"name": "007: Cassino Royale", "name_en": "Casino Royale", "year": 2006, "director": "Martin Campbell", "category": "Acao", "slug": "casino-royale-2006"},
    {"name": "Fogo Contra Fogo", "name_en": "Heat", "year": 1995, "director": "Michael Mann", "category": "Acao", "slug": "heat-1995"},
    {"name": "O Tigre e o Dragao", "name_en": "Crouching Tiger, Hidden Dragon", "year": 2000, "director": "Ang Lee", "category": "Acao", "slug": "crouching-tiger-hidden-dragon-2000"},
    {"name": "Quanto Mais Quente Melhor", "name_en": "Some Like It Hot", "year": 1959, "director": "Billy Wilder", "category": "Comedia", "slug": "some-like-it-hot-1959"},
    {"name": "Curtindo a Vida Adoidado", "name_en": "Ferris Bueller's Day Off", "year": 1986, "director": "John Hughes", "category": "Comedia", "slug": "ferris-buellers-day-off-1986"},
    {"name": "Monty Python em Busca do Calice Sagrado", "name_en": "Monty Python and the Holy Grail", "year": 1975, "director": "Terry Gilliam e Terry Jones", "category": "Comedia", "slug": "monty-python-and-the-holy-grail-1975"},
    {"name": "Superbad: E Hoje", "name_en": "Superbad", "year": 2007, "director": "Greg Mottola", "category": "Comedia", "slug": "superbad-2007"},
    {"name": "Se Beber, Nao Case!", "name_en": "The Hangover", "year": 2009, "director": "Todd Phillips", "category": "Comedia", "slug": "the-hangover-2009"},
    {"name": "O Auto da Compadecida", "name_en": "The Devil's Will", "year": 2000, "director": "Guel Arraes", "category": "Comedia", "slug": "o-auto-da-compadecida-2000"},
    {"name": "Annie Hall: Noivo Neurotico, Noiva Nervosa", "name_en": "Annie Hall", "year": 1977, "director": "Woody Allen", "category": "Comedia", "slug": "annie-hall-1977"},
    {"name": "Feitico do Tempo", "name_en": "Groundhog Day", "year": 1993, "director": "Harold Ramis", "category": "Comedia", "slug": "groundhog-day-1993"},
    {"name": "Debi & Loide: Dois Idiotas em Apuros", "name_en": "Dumb and Dumber", "year": 1994, "director": "Peter Farrelly", "category": "Comedia", "slug": "dumb-and-dumber-1994"},
    {"name": "Meninas Malvadas", "name_en": "Mean Girls", "year": 2004, "director": "Mark Waters", "category": "Comedia", "slug": "mean-girls-2004"},
    {"name": "Apertem os Cintos... O Piloto Sumiu!", "name_en": "Airplane!", "year": 1980, "director": "Jim Abrahams e irmaos Zucker", "category": "Comedia", "slug": "airplane-1980"},
    {"name": "A Vida de Brian", "name_en": "Life of Brian", "year": 1979, "director": "Terry Jones", "category": "Comedia", "slug": "life-of-brian-1979"},
    {"name": "Zoolander", "name_en": "Zoolander", "year": 2001, "director": "Ben Stiller", "category": "Comedia", "slug": "zoolander-2001"},
    {"name": "Quem Vai Ficar com Mary?", "name_en": "There's Something About Mary", "year": 1998, "director": "Peter e Bobby Farrelly", "category": "Comedia", "slug": "theres-something-about-mary-1998"},
    {"name": "Borat", "name_en": "Borat: Cultural Learnings of America", "year": 2006, "director": "Larry Charles", "category": "Comedia", "slug": "borat-2006"},
    {"name": "O Grande Lebowski", "name_en": "The Big Lebowski", "year": 1998, "director": "Joel e Ethan Coen", "category": "Comedia", "slug": "the-big-lebowski-1998"},
    {"name": "Todo Mundo em Panico", "name_en": "Scary Movie", "year": 2000, "director": "Keenen Ivory Wayans", "category": "Comedia", "slug": "scary-movie-2000"},
    {"name": "As Branquelas", "name_en": "White Chicks", "year": 2004, "director": "Keenen Ivory Wayans", "category": "Comedia", "slug": "white-chicks-2004"},
    {"name": "O Virgem de 40 Anos", "name_en": "The 40-Year-Old Virgin", "year": 2005, "director": "Judd Apatow", "category": "Comedia", "slug": "the-40-year-old-virgin-2005"},
    {"name": "Paddington 2", "name_en": "Paddington 2", "year": 2017, "director": "Paul King", "category": "Comedia", "slug": "paddington-2-2017"},
    {"name": "Deadpool", "name_en": "Deadpool", "year": 2016, "director": "Tim Miller", "category": "Comedia", "slug": "deadpool-2016"},
    {"name": "Legalmente Loira", "name_en": "Legally Blonde", "year": 2001, "director": "Robert Luketic", "category": "Comedia", "slug": "legally-blonde-2001"},
    {"name": "American Pie", "name_en": "American Pie", "year": 1999, "director": "Paul Weitz", "category": "Comedia", "slug": "american-pie-1999"},
    {"name": "Um Principe em Nova York", "name_en": "Coming to America", "year": 1988, "director": "John Landis", "category": "Comedia", "slug": "coming-to-america-1988"},
    {"name": "Everything Everywhere All at Once", "name_en": "Everything Everywhere All at Once", "year": 2022, "director": "Daniel Kwan e Daniel Scheinert", "category": "Comedia", "slug": "everything-everywhere-all-at-once-2022"},
    {"name": "Casablanca", "name_en": "Casablanca", "year": 1942, "director": "Michael Curtiz", "category": "Romance", "slug": "casablanca-1942"},
    {"name": "Titanic", "name_en": "Titanic", "year": 1997, "director": "James Cameron", "category": "Romance", "slug": "titanic-1997"},
    {"name": "Antes do Amanhecer", "name_en": "Before Sunrise", "year": 1995, "director": "Richard Linklater", "category": "Romance", "slug": "before-sunrise-1995"},
    {"name": "Brilho Eterno de uma Mente sem Lembrancas", "name_en": "Eternal Sunshine of the Spotless Mind", "year": 2004, "director": "Michel Gondry", "category": "Romance", "slug": "eternal-sunshine-of-the-spotless-mind-2004"},
    {"name": "Orgulho e Preconceito", "name_en": "Pride & Prejudice", "year": 2005, "director": "Joe Wright", "category": "Romance", "slug": "pride-and-prejudice-2005"},
    {"name": "Diario de uma Paixao", "name_en": "The Notebook", "year": 2004, "director": "Nick Cassavetes", "category": "Romance", "slug": "the-notebook-2004"},
    {"name": "La La Land: Cantando Estacoes", "name_en": "La La Land", "year": 2016, "director": "Damien Chazelle", "category": "Romance", "slug": "la-la-land-2016"},
    {"name": "Questao de Tempo", "name_en": "About Time", "year": 2013, "director": "Richard Curtis", "category": "Romance", "slug": "about-time-2013"},
    {"name": "Harry e Sally: Feitos um para o Outro", "name_en": "When Harry Met Sally...", "year": 1989, "director": "Rob Reiner", "category": "Romance", "slug": "when-harry-met-sally-1989"},
    {"name": "Uma Linda Mulher", "name_en": "Pretty Woman", "year": 1990, "director": "Garry Marshall", "category": "Romance", "slug": "pretty-woman-1990"},
    {"name": "10 Coisas Que Eu Odeio em Voce", "name_en": "10 Things I Hate About You", "year": 1999, "director": "Gil Junger", "category": "Romance", "slug": "10-things-i-hate-about-you-1999"},
    {"name": "Como Se Fosse a Primeira Vez", "name_en": "50 First Dates", "year": 2004, "director": "Peter Segal", "category": "Romance", "slug": "50-first-dates-2004"},
    {"name": "P.S. Eu Te Amo", "name_en": "P.S. I Love You", "year": 2007, "director": "Richard LaGravenese", "category": "Romance", "slug": "ps-i-love-you-2007"},
    {"name": "O Segredo de Brokeback Mountain", "name_en": "Brokeback Mountain", "year": 2005, "director": "Ang Lee", "category": "Romance", "slug": "brokeback-mountain-2005"},
    {"name": "Bonequinha de Luxo", "name_en": "Breakfast at Tiffany's", "year": 1961, "director": "Blake Edwards", "category": "Romance", "slug": "breakfast-at-tiffanys-1961"},
    {"name": "Me Chame Pelo Seu Nome", "name_en": "Call Me by Your Name", "year": 2017, "director": "Luca Guadagnino", "category": "Romance", "slug": "call-me-by-your-name-2017"},
    {"name": "Nasce uma Estrela", "name_en": "A Star Is Born", "year": 2018, "director": "Bradley Cooper", "category": "Romance", "slug": "a-star-is-born-2018"},
    {"name": "Sintonizados no Amor", "name_en": "Sleepless in Seattle", "year": 1993, "director": "Nora Ephron", "category": "Romance", "slug": "sleepless-in-seattle-1993"},
    {"name": "Moulin Rouge!", "name_en": "Moulin Rouge!", "year": 2001, "director": "Baz Luhrmann", "category": "Romance", "slug": "moulin-rouge-2001"},
    {"name": "Um Lugar Chamado Notting Hill", "name_en": "Notting Hill", "year": 1999, "director": "Roger Michell", "category": "Romance", "slug": "notting-hill-1999"},
    {"name": "Simplesmente Amor", "name_en": "Love Actually", "year": 2003, "director": "Richard Curtis", "category": "Romance", "slug": "love-actually-2003"},
    {"name": "A Culpa e das Estrelas", "name_en": "The Fault in Our Stars", "year": 2014, "director": "Josh Boone", "category": "Romance", "slug": "the-fault-in-our-stars-2014"},
    {"name": "Your Name", "name_en": "Your Name", "year": 2016, "director": "Makoto Shinkai", "category": "Romance", "slug": "your-name-2016"},
    {"name": "Carol", "name_en": "Carol", "year": 2015, "director": "Todd Haynes", "category": "Romance", "slug": "carol-2015"},
    {"name": "Vidas Passadas", "name_en": "Past Lives", "year": 2023, "director": "Celine Song", "category": "Romance", "slug": "past-lives-2023"},
    {"name": "O Poderoso Chefao", "name_en": "The Godfather", "year": 1972, "director": "Francis Ford Coppola", "category": "Drama", "slug": "the-godfather-1972"},
    {"name": "Um Sonho de Liberdade", "name_en": "The Shawshank Redemption", "year": 1994, "director": "Frank Darabont", "category": "Drama", "slug": "the-shawshank-redemption-1994"},
    {"name": "A Lista de Schindler", "name_en": "Schindler's List", "year": 1993, "director": "Steven Spielberg", "category": "Drama", "slug": "schindlers-list-1993"},
    {"name": "Forrest Gump: O Contador de Historias", "name_en": "Forrest Gump", "year": 1994, "director": "Robert Zemeckis", "category": "Drama", "slug": "forrest-gump-1994"},
    {"name": "Cidade de Deus", "name_en": "City of God", "year": 2002, "director": "Fernando Meirelles e Katia Lund", "category": "Drama", "slug": "city-of-god-2002"},
    {"name": "Clube da Luta", "name_en": "Fight Club", "year": 1999, "director": "David Fincher", "category": "Drama", "slug": "fight-club-1999"},
    {"name": "O Show de Truman", "name_en": "The Truman Show", "year": 1998, "director": "Peter Weir", "category": "Drama", "slug": "the-truman-show-1998"},
    {"name": "Parasita", "name_en": "Parasite", "year": 2019, "director": "Bong Joon-ho", "category": "Drama", "slug": "parasite-2019"},
    {"name": "Beleza Americana", "name_en": "American Beauty", "year": 1999, "director": "Sam Mendes", "category": "Drama", "slug": "american-beauty-1999"},
    {"name": "Coringa", "name_en": "Joker", "year": 2019, "director": "Todd Phillips", "category": "Drama", "slug": "joker-2019"},
    {"name": "Sociedade dos Poetas Mortos", "name_en": "Dead Poets Society", "year": 1989, "director": "Peter Weir", "category": "Drama", "slug": "dead-poets-society-1989"},
    {"name": "Genio Indomavel", "name_en": "Good Will Hunting", "year": 1997, "director": "Gus Van Sant", "category": "Drama", "slug": "good-will-hunting-1997"},
    {"name": "Central do Brasil", "name_en": "Central Station", "year": 1998, "director": "Walter Salles", "category": "Drama", "slug": "central-station-1998"},
    {"name": "O Menino do Pijama Listrado", "name_en": "The Boy in the Striped Pyjamas", "year": 2008, "director": "Mark Herman", "category": "Drama", "slug": "the-boy-in-the-striped-pyjamas-2008"},
    {"name": "O Pianista", "name_en": "The Pianist", "year": 2002, "director": "Roman Polanski", "category": "Drama", "slug": "the-pianist-2002"},
    {"name": "Requiem para um Sonho", "name_en": "Requiem for a Dream", "year": 2000, "director": "Darren Aronofsky", "category": "Drama", "slug": "requiem-for-a-dream-2000"},
    {"name": "O Irlandes", "name_en": "The Irishman", "year": 2019, "director": "Martin Scorsese", "category": "Drama", "slug": "the-irishman-2019"},
    {"name": "Whiplash: Em Busca da Perfeicao", "name_en": "Whiplash", "year": 2014, "director": "Damien Chazelle", "category": "Drama", "slug": "whiplash-2014"},
    {"name": "Roma", "name_en": "Roma", "year": 2018, "director": "Alfonso Cuaron", "category": "Drama", "slug": "roma-2018"},
    {"name": "A Vida e Bela", "name_en": "Life Is Beautiful", "year": 1997, "director": "Roberto Benigni", "category": "Drama", "slug": "life-is-beautiful-1997"},
    {"name": "Moonlight: Sob a Luz do Luar", "name_en": "Moonlight", "year": 2016, "director": "Barry Jenkins", "category": "Drama", "slug": "moonlight-2016"},
    {"name": "12 Anos de Escravidao", "name_en": "12 Years a Slave", "year": 2013, "director": "Steve McQueen", "category": "Drama", "slug": "12-years-a-slave-2013"},
    {"name": "Bastardos Inglorios", "name_en": "Inglourious Basterds", "year": 2009, "director": "Quentin Tarantino", "category": "Drama", "slug": "inglourious-basterds-2009"},
    {"name": "Oppenheimer", "name_en": "Oppenheimer", "year": 2023, "director": "Christopher Nolan", "category": "Drama", "slug": "oppenheimer-2023"},
    {"name": "2001: Uma Odisseia no Espaco", "name_en": "2001: A Space Odyssey", "year": 1968, "director": "Stanley Kubrick", "category": "Ficcao Cientifica", "slug": "2001-a-space-odyssey-1968"},
    {"name": "Blade Runner: O Cacador de Androides", "name_en": "Blade Runner", "year": 1982, "director": "Ridley Scott", "category": "Ficcao Cientifica", "slug": "blade-runner-1982"},
    {"name": "Interestelar", "name_en": "Interstellar", "year": 2014, "director": "Christopher Nolan", "category": "Ficcao Cientifica", "slug": "interstellar-2014"},
    {"name": "A Origem", "name_en": "Inception", "year": 2010, "director": "Christopher Nolan", "category": "Ficcao Cientifica", "slug": "inception-2010"},
    {"name": "Star Wars: Episodio V - O Imperio Contra-Ataca", "name_en": "Star Wars: Episode V - The Empire Strikes Back", "year": 1980, "director": "Irvin Kershner", "category": "Ficcao Cientifica", "slug": "the-empire-strikes-back-1980"},
    {"name": "De Volta para o Futuro", "name_en": "Back to the Future", "year": 1985, "director": "Robert Zemeckis", "category": "Ficcao Cientifica", "slug": "back-to-the-future-1985"},
    {"name": "Duna: Parte Dois", "name_en": "Dune: Part Two", "year": 2024, "director": "Denis Villeneuve", "category": "Ficcao Cientifica", "slug": "dune-part-two-2024"},
    {"name": "O Quinto Elemento", "name_en": "The Fifth Element", "year": 1997, "director": "Luc Besson", "category": "Ficcao Cientifica", "slug": "the-fifth-element-1997"},
    {"name": "E.T.: O Extraterrestre", "name_en": "E.T. the Extra-Terrestrial", "year": 1982, "director": "Steven Spielberg", "category": "Ficcao Cientifica", "slug": "et-the-extra-terrestrial-1982"},
    {"name": "Arrival (A Chegada)", "name_en": "Arrival", "year": 2016, "director": "Denis Villeneuve", "category": "Ficcao Cientifica", "slug": "arrival-2016"},
    {"name": "Minority Report: A Nova Lei", "name_en": "Minority Report", "year": 2002, "director": "Steven Spielberg", "category": "Ficcao Cientifica", "slug": "minority-report-2002"},
    {"name": "Gravidade", "name_en": "Gravity", "year": 2013, "director": "Alfonso Cuaron", "category": "Ficcao Cientifica", "slug": "gravity-2013"},
    {"name": "Distrito 9", "name_en": "District 9", "year": 2009, "director": "Neill Blomkamp", "category": "Ficcao Cientifica", "slug": "district-9-2009"},
    {"name": "Ex Machina: Instinto Artificial", "name_en": "Ex Machina", "year": 2014, "director": "Alex Garland", "category": "Ficcao Cientifica", "slug": "ex-machina-2014"},
    {"name": "Perdido em Marte", "name_en": "The Martian", "year": 2015, "director": "Ridley Scott", "category": "Ficcao Cientifica", "slug": "the-martian-2015"},
    {"name": "Alien, o Oitavo Passageiro", "name_en": "Alien", "year": 1979, "director": "Ridley Scott", "category": "Ficcao Cientifica", "slug": "alien-1979"},
    {"name": "O Vingador do Futuro", "name_en": "Total Recall", "year": 1990, "director": "Paul Verhoeven", "category": "Ficcao Cientifica", "slug": "total-recall-1990"},
    {"name": "RoboCop: O Policial do Futuro", "name_en": "RoboCop", "year": 1987, "director": "Paul Verhoeven", "category": "Ficcao Cientifica", "slug": "robocop-1987"},
    {"name": "Tron: Uma Odisseia Eletronica", "name_en": "Tron", "year": 1982, "director": "Steven Lisberger", "category": "Ficcao Cientifica", "slug": "tron-1982"},
    {"name": "Looper: Assassinos do Futuro", "name_en": "Looper", "year": 2012, "director": "Rian Johnson", "category": "Ficcao Cientifica", "slug": "looper-2012"},
    {"name": "Sob a Pele", "name_en": "Under the Skin", "year": 2013, "director": "Jonathan Glazer", "category": "Ficcao Cientifica", "slug": "under-the-skin-2013"},
    {"name": "Devoradores de Estrelas", "name_en": "Star-Eaters", "year": 2026, "director": "Phil Lord e Christopher Miller", "category": "Ficcao Cientifica", "slug": "star-eaters-2026"},
    {"name": "Tenet", "name_en": "Tenet", "year": 2020, "director": "Christopher Nolan", "category": "Ficcao Cientifica", "slug": "tenet-2020"},
    {"name": "Contato", "name_en": "Contact", "year": 1997, "director": "Robert Zemeckis", "category": "Ficcao Cientifica", "slug": "contact-1997"},
    {"name": "Star Trek", "name_en": "Star Trek", "year": 2009, "director": "J.J. Abrams", "category": "Ficcao Cientifica", "slug": "star-trek-2009"},
    {"name": "A Viagem de Chihiro", "name_en": "Spirited Away", "year": 2001, "director": "Hayao Miyazaki", "category": "Animacao", "slug": "spirited-away-2001"},
    {"name": "O Rei Leao", "name_en": "The Lion King", "year": 1994, "director": "Roger Allers e Rob Minkoff", "category": "Animacao", "slug": "the-lion-king-1994"},
    {"name": "Toy Story", "name_en": "Toy Story", "year": 1995, "director": "John Lasseter", "category": "Animacao", "slug": "toy-story-1995"},
    {"name": "Spider-Man: Across the Spider-Verse", "name_en": "Spider-Man: Across the Spider-Verse", "year": 2023, "director": "Joaquim Dos Santos, Kemp Powers e Justin K. Thompson", "category": "Animacao", "slug": "spider-man-across-the-spider-verse-2023"},
    {"name": "Wall-E", "name_en": "WALL-E", "year": 2008, "director": "Andrew Stanton", "category": "Animacao", "slug": "wall-e-2008"},
    {"name": "Shrek", "name_en": "Shrek", "year": 2001, "director": "Andrew Adamson e Vicky Jenson", "category": "Animacao", "slug": "shrek-2001"},
    {"name": "Procurando Nemo", "name_en": "Finding Nemo", "year": 2003, "director": "Andrew Stanton", "category": "Animacao", "slug": "finding-nemo-2003"},
    {"name": "Divertida Mente", "name_en": "Inside Out", "year": 2015, "director": "Pete Docter", "category": "Animacao", "slug": "inside-out-2015"},
    {"name": "Meu Vizinho Totoro", "name_en": "My Neighbor Totoro", "year": 1988, "director": "Hayao Miyazaki", "category": "Animacao", "slug": "my-neighbor-totoro-1988"},
    {"name": "Up: Altas Aventuras", "name_en": "Up", "year": 2009, "director": "Pete Docter", "category": "Animacao", "slug": "up-2009"},
    {"name": "Os Incriveis", "name_en": "The Incredibles", "year": 2004, "director": "Brad Bird", "category": "Animacao", "slug": "the-incredibles-2004"},
    {"name": "Como Treinar o Seu Dragao", "name_en": "How to Train Your Dragon", "year": 2010, "director": "Chris Sanders e Dean DeBlois", "category": "Animacao", "slug": "how-to-train-your-dragon-2010"},
    {"name": "Monstros S.A.", "name_en": "Monsters, Inc.", "year": 2001, "director": "Pete Docter", "category": "Animacao", "slug": "monsters-inc-2001"},
    {"name": "Ratatouille", "name_en": "Ratatouille", "year": 2007, "director": "Brad Bird", "category": "Animacao", "slug": "ratatouille-2007"},
    {"name": "Pinoquio por Guillermo del Toro", "name_en": "Guillermo del Toro's Pinocchio", "year": 2022, "director": "Guillermo del Toro e Mark Gustafson", "category": "Animacao", "slug": "guillermo-del-toros-pinocchio-2022"},
    {"name": "O Gigante de Ferro", "name_en": "The Iron Giant", "year": 1999, "director": "Brad Bird", "category": "Animacao", "slug": "the-iron-giant-1999"},
    {"name": "Akira", "name_en": "Akira", "year": 1988, "director": "Katsuhiro Otomo", "category": "Animacao", "slug": "akira-1988"},
    {"name": "Klaus", "name_en": "Klaus", "year": 2019, "director": "Sergio Pablos", "category": "Animacao", "slug": "klaus-2019"},
    {"name": "Zootopia", "name_en": "Zootopia", "year": 2016, "director": "Byron Howard e Rich Moore", "category": "Animacao", "slug": "zootopia-2016"},
    {"name": "Soul", "name_en": "Soul", "year": 2020, "director": "Pete Docter", "category": "Animacao", "slug": "soul-2020"},
    {"name": "A Bela e a Fera", "name_en": "Beauty and the Beast", "year": 1991, "director": "Gary Trousdale e Kirk Wise", "category": "Animacao", "slug": "beauty-and-the-beast-1991"},
    {"name": "Coco (Viva: A Vida e uma Festa)", "name_en": "Coco", "year": 2017, "director": "Lee Unkrich", "category": "Animacao", "slug": "coco-2017"},
    {"name": "Guerreiras do K-Pop", "name_en": "K-Pop Warriors", "year": 2026, "director": "Maggie Kang e Chris Appelhans", "category": "Animacao", "slug": "k-pop-warriors-2026"},
    {"name": "O Menino e a Garca", "name_en": "The Boy and the Heron", "year": 2023, "director": "Hayao Miyazaki", "category": "Animacao", "slug": "the-boy-and-the-heron-2023"},
    {"name": "Super Mario Galaxy: O Filme", "name_en": "Super Mario Galaxy: The Movie", "year": 2026, "director": "Aaron Horvath e Michael Jelenic", "category": "Animacao", "slug": "super-mario-galaxy-the-movie-2026"},
    {"name": "Blade Runner 2049", "name_en": "Blade Runner 2049", "year": 2017, "director": "Denis Villeneuve", "category": "Distopia", "slug": "blade-runner-2049-2017"},
    {"name": "Filhos da Esperanca", "name_en": "Children of Men", "year": 2006, "director": "Alfonso Cuaron", "category": "Distopia", "slug": "children-of-men-2006"},
    {"name": "Laranja Mecanica", "name_en": "A Clockwork Orange", "year": 1971, "director": "Stanley Kubrick", "category": "Distopia", "slug": "a-clockwork-orange-1971"},
    {"name": "1984", "name_en": "1984", "year": 1984, "director": "Michael Radford", "category": "Distopia", "slug": "1984-1984"},
    {"name": "Jogos Vorazes", "name_en": "The Hunger Games", "year": 2012, "director": "Gary Ross", "category": "Distopia", "slug": "the-hunger-games-2012"},
    {"name": "V de Vinganca", "name_en": "V for Vendetta", "year": 2005, "director": "James McTeigue", "category": "Distopia", "slug": "v-for-vendetta-2005"},
    {"name": "O Exterminador do Futuro", "name_en": "The Terminator", "year": 1984, "director": "James Cameron", "category": "Distopia", "slug": "the-terminator-1984"},
    {"name": "Expresso do Amanha", "name_en": "Snowpiercer", "year": 2013, "director": "Bong Joon-ho", "category": "Distopia", "slug": "snowpiercer-2013"},
    {"name": "Fahrenheit 451", "name_en": "Fahrenheit 451", "year": 1966, "director": "Francois Truffaut", "category": "Distopia", "slug": "fahrenheit-451-1966"},
    {"name": "Metropolis", "name_en": "Metropolis", "year": 1927, "director": "Fritz Lang", "category": "Distopia", "slug": "metropolis-1927"},
    {"name": "O Sobrevivente", "name_en": "The Running Man", "year": 1987, "director": "Paul Michael Glaser", "category": "Distopia", "slug": "the-running-man-1987"},
    {"name": "Gattaca: A Experiencia Genetica", "name_en": "Gattaca", "year": 1997, "director": "Andrew Niccol", "category": "Distopia", "slug": "gattaca-1997"},
    {"name": "O Conto da Aia", "name_en": "The Handmaid's Tale", "year": 1990, "director": "Volker Schlondorff", "category": "Distopia", "slug": "the-handmaids-tale-1990"},
    {"name": "Mad Max 2: A Cacada Continua", "name_en": "Mad Max 2", "year": 1981, "director": "George Miller", "category": "Distopia", "slug": "mad-max-2-1981"},
    {"name": "Elysium", "name_en": "Elysium", "year": 2013, "director": "Neill Blomkamp", "category": "Distopia", "slug": "elysium-2013"},
    {"name": "Matrix Resurrections", "name_en": "The Matrix Resurrections", "year": 2021, "director": "Lana Wachowski", "category": "Distopia", "slug": "the-matrix-resurrections-2021"},
    {"name": "Brazil: O Filme", "name_en": "Brazil", "year": 1985, "director": "Terry Gilliam", "category": "Distopia", "slug": "brazil-1985"},
    {"name": "Equilibrium", "name_en": "Equilibrium", "year": 2002, "director": "Kurt Wimmer", "category": "Distopia", "slug": "equilibrium-2002"},
    {"name": "Battle Royale", "name_en": "Battle Royale", "year": 2000, "director": "Kinji Fukasaku", "category": "Distopia", "slug": "battle-royale-2000"},
    {"name": "Idiocracia", "name_en": "Idiocracy", "year": 2006, "director": "Mike Judge", "category": "Distopia", "slug": "idiocracy-2006"},
    {"name": "O Planeta dos Macacos", "name_en": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner", "category": "Distopia", "slug": "planet-of-the-apes-1968"},
    {"name": "2067", "name_en": "2067", "year": 2020, "director": "Seth Larney", "category": "Distopia", "slug": "2067-2020"},
    {"name": "Divergente", "name_en": "Divergent", "year": 2014, "director": "Neil Burger", "category": "Distopia", "slug": "divergent-2014"},
    {"name": "Minority Report: A Nova Lei", "name_en": "Minority Report", "year": 2002, "director": "Steven Spielberg", "category": "Distopia", "slug": "minority-report-2002"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.svg')

def is_image_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    return path.endswith(IMAGE_EXTENSIONS)

def fetch_image_urls(slug: str):
    url = f"https://movie-screencaps.com/{slug}/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Erro ao processar a pesquisa: {str(e)}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    # Filtra apenas URLs que terminam com extensao de imagem (ignorando query string)
    images = [a["href"] for a in soup.find_all("a", href=True) if is_image_url(a["href"])]
    return list(dict.fromkeys(images))

# =============================================================================
# TMDB FALLBACK FUNCTIONS
# =============================================================================

def search_tmdb_movie(name_en: str, year: int):
    """Busca o filme no TMDB pelo nome em ingles + ano. Retorna o movie_id ou None."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": name_en, "year": year}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if results:
            # Pega o primeiro resultado (melhor match)
            return results[0]["id"]
    except Exception as e:
        logging.error(f"  [TMDB] Erro na busca por '{name_en}': {str(e)}")
    return None

def fetch_tmdb_backdrops(movie_id: int):
    """Busca backdrops do filme no TMDB. Retorna lista de URLs completas."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/images"
    params = {"api_key": TMDB_API_KEY}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        backdrops = data.get("backdrops", [])
        # Ordena por vote_average decrescente para pegar as melhores imagens primeiro
        backdrops.sort(key=lambda x: x.get("vote_average", 0), reverse=True)
        urls = [f"https://image.tmdb.org/t/p/{TMDB_IMAGE_SIZE}{b['file_path']}" for b in backdrops]
        return urls
    except Exception as e:
        logging.error(f"  [TMDB] Erro ao buscar imagens do movie_id {movie_id}: {str(e)}")
    return []

def fetch_movie_images(movie: dict):
    """
    Tenta buscar imagens em duas fontes:
    1. movie-screencaps.com (slug)
    2. TMDB fallback (name_en + year)
    
    Retorna: (lista_urls, nome_fonte)
    nome_fonte pode ser: "movie-screencaps", "tmdb", ou "none"
    """
    slug = movie["slug"]
    name_en = movie["name_en"]
    year = movie["year"]
    
    # Fonte 1: movie-screencaps.com
    logging.info(f"  [Fonte 1] Buscando no movie-screencaps.com...")
    urls = fetch_image_urls(slug)
    if len(urls) >= 15:
        logging.info(f"  [Fonte 1] Sucesso: {len(urls)} imagens encontradas")
        return urls, "movie-screencaps"
    
    logging.warning(f"  [Fonte 1] Insuficiente: {len(urls)} imagens. Tentando fallback TMDB...")
    
    # Fonte 2: TMDB fallback
    movie_id = search_tmdb_movie(name_en, year)
    if movie_id:
        logging.info(f"  [Fonte 2] TMDB movie_id encontrado: {movie_id}")
        tmdb_urls = fetch_tmdb_backdrops(movie_id)
        if len(tmdb_urls) >= 15:
            logging.info(f"  [Fonte 2] Sucesso TMDB: {len(tmdb_urls)} backdrops encontrados")
            return tmdb_urls, "tmdb"
        logging.warning(f"  [Fonte 2] TMDB tambem insuficiente: {len(tmdb_urls)} backdrops")
    else:
        logging.warning(f"  [Fonte 2] Filme nao encontrado no TMDB")
    
    return [], "none"

# =============================================================================

def distribute_difficulty(images: list):
    total = len(images)
    if total < 15:
        return [], 0, 0, 0

    if total >= 15:
        easy, medium, hard = images[0:5], images[total // 2 - 2:total // 2 + 3], images[-5:]
    else:
        n = total // 3
        easy, medium, hard = images[0:n], images[n:2 * n], images[2 * n:]

    res = []
    for i, url in enumerate(easy):
        res.append({"path": url, "difficulty": "EASY", "order": i})
    for i, url in enumerate(medium):
        res.append({"path": url, "difficulty": "MEDIUM", "order": i + 5})
    for i, url in enumerate(hard):
        res.append({"path": url, "difficulty": "HARD", "order": i + 10})

    return res, len(easy), len(medium), len(hard)

def main():
    final_data = {"status": "success", "processed_movies": [], "failed_movies": []}

    logging.info("\n--- INICIANDO PROCESSO DE SCRAPPING ---")

    for movie in MOVIES:
        logging.info(f"Processando: {movie['name']}")
        urls, source = fetch_movie_images(movie)
        total_recuperado = len(urls)

        # LOG 1: Total de imagens recuperadas
        logging.info(f"  [LOG] Total de imagens recuperadas ({source}): {total_recuperado}")

        if total_recuperado < 15:
            reason = "Nao encontrado em nenhuma fonte" if total_recuperado == 0 else f"Imagens insuficientes ({total_recuperado})"
            final_data["failed_movies"].append({"name": movie["name"], "name_english": movie["name_en"]})
            logging.warning(f"  Filme ignorado: {reason}")
            continue

        images, q_easy, q_med, q_hard = distribute_difficulty(urls)

        # LOG 2: Distribuicao por dificuldade
        logging.info(f"  [LOG] Distribuicao final -> EASY: {q_easy} | MEDIUM: {q_med} | HARD: {q_hard}")
        logging.info(f"  [LOG] Fonte utilizada: {source}")

        final_data["processed_movies"].append({
            "name": movie["name"],
            "name_en": movie["name_en"],
            "year": movie["year"],
            "director": movie["director"],
            "category": movie["category"],
            "images": images
        })
        time.sleep(1.5)

    with open("movies_report.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    logging.info(f"--- FIM DO PROCESSO. Sucessos: {len(final_data['processed_movies'])} | Falhas: {len(final_data['failed_movies'])} ---")

if __name__ == "__main__":
    main()
