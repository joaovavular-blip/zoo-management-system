"""Gera um zoo"""

import random

NUM_ZONAS = 7

types = [
    "Aves",
    "Carnívoros",
    "Herbívoros",
    "Mamíferos Marinhos",
    "Primatas",
    "Repteis"
]

continents = [
    "África",
    "América",
    "Asia",
    "Austrália",
    "Europa"
]

def sql_str(valor):
    if valor is None:
        return "NULL"
    return f"'{valor}'"


def gerar_zonas(tipos, continentes):
    tipos = tipos.copy()
    continentes = continentes.copy()
    zonas_info = []

    especialidade = continentes.pop(random.randint(0, len(continentes) - 1))

    tipo1 = tipos.pop(random.randint(0, len(tipos) - 1))
    tipo2 = tipos.pop(random.randint(0, len(tipos) - 1))
    tipo3 = tipos.pop(random.randint(0, len(tipos) - 1))
    tipo4 = tipos.pop(random.randint(0, len(tipos) - 1))
    tipo5 = tipos.pop(random.randint(0, len(tipos) - 1))

    continente1 = continentes.pop(random.randint(0, len(continentes) - 1))
    continente2 = continentes.pop(random.randint(0, len(continentes) - 1))

    print(f"INSERT INTO zona VALUES (1, {sql_str(tipo1)}, {sql_str(especialidade)}, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([1, tipo1, especialidade])

    print(f"INSERT INTO zona VALUES (2, {sql_str(tipo2)}, {sql_str(especialidade)}, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([2, tipo2, especialidade])

    print(f"INSERT INTO zona VALUES (3, {sql_str(tipo3)}, NULL, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([3, tipo3, None])

    print(f"INSERT INTO zona VALUES (4, {sql_str(tipo4)}, NULL, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([4, tipo4, None])

    print(f"INSERT INTO zona VALUES (5, {sql_str(tipo5)}, NULL, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([5, tipo5, None])

    print(f"INSERT INTO zona VALUES (6, NULL, {sql_str(continente1)}, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([6, None, continente1])

    print(f"INSERT INTO zona VALUES (7, NULL, {sql_str(continente2)}, {round(5 + random.random() * 25, 2)});")
    zonas_info.append([7, None, continente2])

    proximo_id = 8

    while proximo_id <= NUM_ZONAS and len(continentes) > 0:
        continente = continentes.pop(random.randint(0, len(continentes) - 1))
        preco = round(5 + random.random() * 25, 2)

        print(f"INSERT INTO zona VALUES ({proximo_id}, NULL, {sql_str(continente)}, {preco});")
        zonas_info.append([proximo_id, None, continente])

        proximo_id += 1

    while proximo_id <= NUM_ZONAS and len(tipos) > 0:
        tipo = tipos.pop(random.randint(0, len(tipos) - 1))
        preco = round(5 + random.random() * 25, 2)

        print(f"INSERT INTO zona VALUES ({proximo_id}, {sql_str(tipo)}, NULL, {preco});")
        zonas_info.append([proximo_id, tipo, None])

        proximo_id += 1

    if proximo_id <= NUM_ZONAS:
        raise ValueError("Não há continentes/categorias suficientes para criar zonas extra sem repetir.")

    return zonas_info
    
PERCENTAGEM_MIN_NUMERO_DE_VOTOS=0.1
MIN_RECITOS_POR_ZONA=10
MAX_RECINTOS_POR_ZONA=30

def gerar_recintos():
    id_recinto = 1
    recintos = []

    for id_zona in range(1, NUM_ZONAS + 1):
        numero_recintos = 2

        for _ in range(numero_recintos):
            votos = 0

            print(f"INSERT INTO recinto VALUES ({id_recinto}, {id_zona}, {votos});")

            recintos.append([id_recinto, id_zona, 0])
            id_recinto += 1
            
    return recintos

def votar_em_recinto(zonas_nao_acessadas, total_de_bilhetes):
    estimativa_min_votos_float = total_de_bilhetes / 100 * PERCENTAGEM_MIN_NUMERO_DE_VOTOS
    estimativa_min_votos = int(estimativa_min_votos_float)

    if estimativa_min_votos < estimativa_min_votos_float:
        estimativa_min_votos += 1

    zonas_acessadas = set(range(1, NUM_ZONAS + 1)) - set(zonas_nao_acessadas)

    indexs = []

    for index, recinto in enumerate(lista_recintos):
        if recinto[1] in zonas_acessadas:
            indexs.append(index)

            if recinto[2] < estimativa_min_votos:
                recinto[2] += 1
                return

    if len(indexs) == 0:
        raise ValueError("O bilhete não tem acesso a nenhum recinto.")

    index_escolhido = random.choice(indexs)
    lista_recintos[index_escolhido][2] += 1


#pode criar uma situaçao em q numero de acessos < votos mas isso é extremamente raro
def atualizar_votos_recintos(total_votos):
    min_votos_float=total_votos/100*PERCENTAGEM_MIN_NUMERO_DE_VOTOS
    min_votos=int(min_votos_float)

    if min_votos<min_votos_float:
        min_votos+=1

    numero_recintos=len(lista_recintos)

    if min_votos*numero_recintos>total_votos:
        raise ValueError("Não há votos suficientes para garantir o mínimo em todos os recintos.")

    broken=True

    while broken:
        broken=False

        for index, recinto in enumerate(lista_recintos):
            if recinto[2]<min_votos:
                broken=True

                index_max=None
                max_votos=min_votos

                for index_0, outro_recinto in enumerate(lista_recintos):
                    if outro_recinto[2]>max_votos:
                        index_max=index_0
                        max_votos=outro_recinto[2]

                if index_max is None:
                    raise ValueError("Não foi possível redistribuir votos sem quebrar o mínimo.")

                lista_recintos[index_max][2]-=1
                lista_recintos[index][2]+=1

    for id_recinto, id_zona, votos in lista_recintos:
        print(f"UPDATE recinto SET votos = {votos} WHERE id_recinto = {id_recinto};")


especies_base = [
    ("Panthera leo", "Leão", "Carnívoros"),
    ("Panthera tigris", "Tigre", "Carnívoros"),
    ("Panthera pardus", "Leopardo", "Carnívoros"),
    ("Panthera onca", "Jaguar", "Carnívoros"),
    ("Panthera uncia", "Leopardo-das-neves", "Carnívoros"),
    ("Acinonyx jubatus", "Chita", "Carnívoros"),
    ("Puma concolor", "Puma", "Carnívoros"),
    ("Lynx lynx", "Lince-euroasiático", "Carnívoros"),
    ("Lynx pardinus", "Lince-ibérico", "Carnívoros"),
    ("Caracal caracal", "Caracal", "Carnívoros"),
    ("Leopardus pardalis", "Jaguatirica", "Carnívoros"),
    ("Neofelis nebulosa", "Pantera-nebulosa", "Carnívoros"),
    ("Felis catus", "Gato-doméstico", "Carnívoros"),
    ("Canis lupus", "Lobo-cinzento", "Carnívoros"),
    ("Canis latrans", "Coiote", "Carnívoros"),
    ("Canis aureus", "Chacal-dourado", "Carnívoros"),
    ("Vulpes vulpes", "Raposa-vermelha", "Carnívoros"),
    ("Vulpes zerda", "Feneco", "Carnívoros"),
    ("Lycaon pictus", "Mabeco", "Carnívoros"),
    ("Cuon alpinus", "Cão-selvagem-asiático", "Carnívoros"),
    ("Ursus arctos", "Urso-pardo", "Carnívoros"),
    ("Ursus maritimus", "Urso-polar", "Carnívoros"),
    ("Ursus americanus", "Urso-negro-americano", "Carnívoros"),
    ("Ailuropoda melanoleuca", "Panda-gigante", "Carnívoros"),
    ("Helarctos malayanus", "Urso-malaio", "Carnívoros"),
    ("Melursus ursinus", "Urso-beiçudo", "Carnívoros"),
    ("Tremarctos ornatus", "Urso-de-óculos", "Carnívoros"),
    ("Mustela putorius", "Toirão", "Carnívoros"),
    ("Mustela nivalis", "Doninha", "Carnívoros"),
    ("Meles meles", "Texugo-europeu", "Carnívoros"),
    ("Lutra lutra", "Lontra-europeia", "Carnívoros"),
    ("Enhydra lutris", "Lontra-marinha", "Carnívoros"),
    ("Gulo gulo", "Glutão", "Carnívoros"),
    ("Mephitis mephitis", "Gambá-listrado", "Carnívoros"),
    ("Procyon lotor", "Guaxinim", "Carnívoros"),
    ("Nasua nasua", "Quati", "Carnívoros"),
    ("Suricata suricatta", "Suricata", "Carnívoros"),
    ("Crocuta crocuta", "Hiena-malhada", "Carnívoros"),
    ("Hyaena hyaena", "Hiena-riscada", "Carnívoros"),
    ("Herpestes ichneumon", "Saca-rabos", "Carnívoros"),

    ("Loxodonta africana", "Elefante-africano", "Herbívoros"),
    ("Elephas maximus", "Elefante-asiático", "Herbívoros"),
    ("Giraffa camelopardalis", "Girafa", "Herbívoros"),
    ("Okapia johnstoni", "Ocapi", "Herbívoros"),
    ("Hippopotamus amphibius", "Hipopótamo", "Herbívoros"),
    ("Choeropsis liberiensis", "Hipopótamo-pigmeu", "Herbívoros"),
    ("Ceratotherium simum", "Rinoceronte-branco", "Herbívoros"),
    ("Diceros bicornis", "Rinoceronte-negro", "Herbívoros"),
    ("Rhinoceros unicornis", "Rinoceronte-indiano", "Herbívoros"),
    ("Equus quagga", "Zebra-das-planícies", "Herbívoros"),
    ("Equus grevyi", "Zebra-de-grevy", "Herbívoros"),
    ("Equus ferus", "Cavalo-selvagem", "Herbívoros"),
    ("Tapirus terrestris", "Anta-brasileira", "Herbívoros"),
    ("Tapirus indicus", "Anta-malaia", "Herbívoros"),
    ("Sus scrofa", "Javali", "Herbívoros"),
    ("Phacochoerus africanus", "Facocero", "Herbívoros"),
    ("Potamochoerus porcus", "Porco-vermelho-do-rio", "Herbívoros"),
    ("Camelus dromedarius", "Dromedário", "Herbívoros"),
    ("Camelus bactrianus", "Camelo-bactriano", "Herbívoros"),
    ("Lama glama", "Lhama", "Herbívoros"),
    ("Vicugna vicugna", "Vicunha", "Herbívoros"),
    ("Bison bison", "Bisão-americano", "Herbívoros"),
    ("Bison bonasus", "Bisão-europeu", "Herbívoros"),
    ("Syncerus caffer", "Búfalo-africano", "Herbívoros"),
    ("Bubalus bubalis", "Búfalo-asiático", "Herbívoros"),
    ("Bos grunniens", "Iaque", "Herbívoros"),
    ("Ovis aries", "Ovelha-doméstica", "Herbívoros"),
    ("Ovis canadensis", "Carneiro-selvagem", "Herbívoros"),
    ("Capra ibex", "Íbex", "Herbívoros"),
    ("Capra hircus", "Cabra-doméstica", "Herbívoros"),
    ("Gazella dorcas", "Gazela-dorcas", "Herbívoros"),
    ("Nanger dama", "Gazela-dama", "Herbívoros"),
    ("Antilope cervicapra", "Antílope-negro", "Herbívoros"),
    ("Connochaetes taurinus", "Gnu-azul", "Herbívoros"),
    ("Connochaetes gnou", "Gnu-de-cauda-branca", "Herbívoros"),
    ("Oryx gazella", "Órix", "Herbívoros"),
    ("Addax nasomaculatus", "Addax", "Herbívoros"),
    ("Hippotragus niger", "Palanca-negra", "Herbívoros"),
    ("Alces alces", "Alce", "Herbívoros"),
    ("Rangifer tarandus", "Rena", "Herbívoros"),
    ("Cervus elaphus", "Veado-vermelho", "Herbívoros"),
    ("Dama dama", "Gamo", "Herbívoros"),
    ("Capreolus capreolus", "Corço", "Herbívoros"),
    ("Odocoileus virginianus", "Veado-de-cauda-branca", "Herbívoros"),
    ("Macropus rufus", "Canguru-vermelho", "Herbívoros"),
    ("Macropus giganteus", "Canguru-cinzento-oriental", "Herbívoros"),
    ("Phascolarctos cinereus", "Coala", "Herbívoros"),
    ("Vombatus ursinus", "Vombate-comum", "Herbívoros"),
    ("Sarcophilus harrisii", "Diabo-da-tasmânia", "Carnívoros"),
    ("Trichosurus vulpecula", "Gambá-australiano", "Herbívoros"),

    ("Gorilla gorilla", "Gorila-ocidental", "Primatas"),
    ("Gorilla beringei", "Gorila-oriental", "Primatas"),
    ("Pan troglodytes", "Chimpanzé", "Primatas"),
    ("Pan paniscus", "Bonobo", "Primatas"),
    ("Pongo pygmaeus", "Orangotango-do-bornéu", "Primatas"),
    ("Pongo abelii", "Orangotango-de-sumatra", "Primatas"),
    ("Hylobates lar", "Gibão-de-mãos-brancas", "Primatas"),
    ("Papio anubis", "Babuíno-anúbis", "Primatas"),
    ("Papio hamadryas", "Babuíno-sagrado", "Primatas"),
    ("Mandrillus sphinx", "Mandril", "Primatas"),
    ("Mandrillus leucophaeus", "Dril", "Primatas"),
    ("Macaca mulatta", "Macaco-rhesus", "Primatas"),
    ("Macaca fascicularis", "Macaco-caranguejeiro", "Primatas"),
    ("Macaca sylvanus", "Macaco-de-gibraltar", "Primatas"),
    ("Cercopithecus neglectus", "Macaco-de-brazza", "Primatas"),
    ("Chlorocebus pygerythrus", "Macaco-vervet", "Primatas"),
    ("Colobus guereza", "Colobo-preto-e-branco", "Primatas"),
    ("Nasalis larvatus", "Macaco-narigudo", "Primatas"),
    ("Ateles geoffroyi", "Macaco-aranha", "Primatas"),
    ("Alouatta caraya", "Bugio-preto", "Primatas"),
    ("Cebus capucinus", "Macaco-prego-de-cara-branca", "Primatas"),
    ("Sapajus apella", "Macaco-prego", "Primatas"),
    ("Saimiri sciureus", "Macaco-de-cheiro", "Primatas"),
    ("Callithrix jacchus", "Sagui-comum", "Primatas"),
    ("Leontopithecus rosalia", "Mico-leão-dourado", "Primatas"),
    ("Saguinus oedipus", "Mico-leão-de-cara-branca", "Primatas"),
    ("Lemur catta", "Lémure-de-cauda-anelada", "Primatas"),
    ("Varecia variegata", "Lémure-variegado-preto-e-branco", "Primatas"),
    ("Eulemur fulvus", "Lémure-pardo", "Primatas"),
    ("Daubentonia madagascariensis", "Aie-aie", "Primatas"),

    ("Struthio camelus", "Avestruz", "Aves"),
    ("Dromaius novaehollandiae", "Ema", "Aves"),
    ("Casuarius casuarius", "Casuar-do-sul", "Aves"),
    ("Rhea americana", "Ema-americana", "Aves"),
    ("Aptenodytes forsteri", "Pinguim-imperador", "Aves"),
    ("Aptenodytes patagonicus", "Pinguim-rei", "Aves"),
    ("Spheniscus demersus", "Pinguim-africano", "Aves"),
    ("Spheniscus magellanicus", "Pinguim-de-magalhães", "Aves"),
    ("Pelecanus onocrotalus", "Pelicano-branco", "Aves"),
    ("Pelecanus occidentalis", "Pelicano-pardo", "Aves"),
    ("Phoenicopterus roseus", "Flamingo-comum", "Aves"),
    ("Phoenicopterus ruber", "Flamingo-americano", "Aves"),
    ("Ciconia ciconia", "Cegonha-branca", "Aves"),
    ("Leptoptilos crumenifer", "Marabu-africano", "Aves"),
    ("Ardea cinerea", "Garça-real", "Aves"),
    ("Bubulcus ibis", "Garça-boieira", "Aves"),
    ("Threskiornis aethiopicus", "Íbis-sagrado", "Aves"),
    ("Platalea leucorodia", "Colhereiro", "Aves"),
    ("Cygnus olor", "Cisne-branco", "Aves"),
    ("Anas platyrhynchos", "Pato-real", "Aves"),
    ("Branta canadensis", "Ganso-do-canadá", "Aves"),
    ("Aquila chrysaetos", "Águia-real", "Aves"),
    ("Haliaeetus leucocephalus", "Águia-de-cabeça-branca", "Aves"),
    ("Gyps fulvus", "Grifo", "Aves"),
    ("Gypaetus barbatus", "Quebra-ossos", "Aves"),
    ("Falco peregrinus", "Falcão-peregrino", "Aves"),
    ("Bubo bubo", "Bufo-real", "Aves"),
    ("Tyto alba", "Coruja-das-torres", "Aves"),
    ("Pavo cristatus", "Pavão-indiano", "Aves"),
    ("Gallus gallus", "Galo-selvagem", "Aves"),
    ("Meleagris gallopavo", "Peru-selvagem", "Aves"),
    ("Grus grus", "Grou-comum", "Aves"),
    ("Balearica regulorum", "Grou-coroado-cinzento", "Aves"),
    ("Ara ararauna", "Arara-canindé", "Aves"),
    ("Ara macao", "Arara-vermelha", "Aves"),
    ("Amazona aestiva", "Papagaio-verdadeiro", "Aves"),
    ("Psittacus erithacus", "Papagaio-cinzento", "Aves"),
    ("Cacatua galerita", "Cacatua-de-crista-amarela", "Aves"),
    ("Ramphastos toco", "Tucano-toco", "Aves"),
    ("Tauraco persa", "Turaco-verde", "Aves"),
    ("Alcedo atthis", "Guarda-rios", "Aves"),
    ("Corvus corax", "Corvo-comum", "Aves"),
    ("Pica pica", "Pega-rabuda", "Aves"),

    ("Crocodylus niloticus", "Crocodilo-do-nilo", "Repteis"),
    ("Crocodylus porosus", "Crocodilo-de-água-salgada", "Repteis"),
    ("Crocodylus acutus", "Crocodilo-americano", "Repteis"),
    ("Alligator mississippiensis", "Aligátor-americano", "Repteis"),
    ("Caiman crocodilus", "Jacaré-tinga", "Repteis"),
    ("Gavialis gangeticus", "Gavial", "Repteis"),
    ("Varanus komodoensis", "Dragão-de-komodo", "Repteis"),
    ("Varanus niloticus", "Varano-do-nilo", "Repteis"),
    ("Iguana iguana", "Iguana-verde", "Repteis"),
    ("Cyclura cornuta", "Iguana-rinoceronte", "Repteis"),
    ("Pogona vitticeps", "Dragão-barbudo", "Repteis"),
    ("Chamaeleo calyptratus", "Camaleão-do-yémen", "Repteis"),
    ("Furcifer pardalis", "Camaleão-pantera", "Repteis"),
    ("Eublepharis macularius", "Osga-leopardo", "Repteis"),
    ("Gekko gecko", "Osga-tokay", "Repteis"),
    ("Python regius", "Píton-real", "Repteis"),
    ("Python bivittatus", "Píton-birmanesa", "Repteis"),
    ("Boa constrictor", "Jiboia", "Repteis"),
    ("Eunectes murinus", "Anaconda-verde", "Repteis"),
    ("Naja naja", "Cobra-capelo-indiana", "Repteis"),
    ("Ophiophagus hannah", "Cobra-rei", "Repteis"),
    ("Dendroaspis polylepis", "Mamba-negra", "Repteis"),
    ("Crotalus atrox", "Cascavel-diamante-ocidental", "Repteis"),
    ("Bitis arietans", "Víbora-sopradora", "Repteis"),
    ("Chelonoidis niger", "Tartaruga-gigante-de-galápagos", "Repteis"),
    ("Aldabrachelys gigantea", "Tartaruga-gigante-de-aldabra", "Repteis"),
    ("Testudo graeca", "Tartaruga-moura", "Repteis"),
    ("Testudo hermanni", "Tartaruga-mediterrânica", "Repteis"),
    ("Chelonia mydas", "Tartaruga-verde", "Repteis"),
    ("Caretta caretta", "Tartaruga-comum", "Repteis"),
    ("Eretmochelys imbricata", "Tartaruga-de-pente", "Repteis"),

    ("Balaenoptera musculus", "Baleia-azul", "Mamíferos Marinhos"),
    ("Balaenoptera physalus", "Baleia-comum", "Mamíferos Marinhos"),
    ("Megaptera novaeangliae", "Baleia-jubarte", "Mamíferos Marinhos"),
    ("Eschrichtius robustus", "Baleia-cinzenta", "Mamíferos Marinhos"),
    ("Physeter macrocephalus", "Cachalote", "Mamíferos Marinhos"),
    ("Orcinus orca", "Orca", "Mamíferos Marinhos"),
    ("Delphinus delphis", "Golfinho-comum", "Mamíferos Marinhos"),
    ("Tursiops truncatus", "Golfinho-roaz", "Mamíferos Marinhos"),
    ("Stenella longirostris", "Golfinho-rotador", "Mamíferos Marinhos"),
    ("Globicephala melas", "Baleia-piloto", "Mamíferos Marinhos"),
    ("Grampus griseus", "Golfinho-de-risso", "Mamíferos Marinhos"),
    ("Phocoena phocoena", "Boto", "Mamíferos Marinhos"),
    ("Monodon monoceros", "Narval", "Mamíferos Marinhos"),
    ("Delphinapterus leucas", "Beluga", "Mamíferos Marinhos"),
    ("Odobenus rosmarus", "Morsa", "Mamíferos Marinhos"),
    ("Mirounga leonina", "Elefante-marinho-do-sul", "Mamíferos Marinhos"),
    ("Halichoerus grypus", "Foca-cinzenta", "Mamíferos Marinhos"),
    ("Phoca vitulina", "Foca-comum", "Mamíferos Marinhos"),
    ("Hydrurga leptonyx", "Foca-leopardo", "Mamíferos Marinhos"),
    ("Zalophus californianus", "Leão-marinho-da-califórnia", "Mamíferos Marinhos"),
    ("Otaria flavescens", "Leão-marinho-sul-americano", "Mamíferos Marinhos"),
    ("Arctocephalus pusillus", "Lobo-marinho-sul-africano", "Mamíferos Marinhos"),
    ("Trichechus manatus", "Manatim-das-caraíbas", "Mamíferos Marinhos"),
    ("Dugong dugon", "Dugongo", "Mamíferos Marinhos")
]

def escolher_continente_para_especie(categoria, zonas_info):
    zonas_compativeis = []

    for id_zona, categoria_zona, continente_zona in zonas_info:
        if categoria_zona == categoria or categoria_zona is None:
            zonas_compativeis.append([id_zona, categoria_zona, continente_zona])

    if len(zonas_compativeis) == 0:
        raise ValueError(f"Não há nenhuma zona compatível com a categoria {categoria}.")

    zona_escolhida = random.choice(zonas_compativeis)

    if zona_escolhida[2] is None:
        continente = random.choice(continents)
    else:
        continente = zona_escolhida[2]

    return continente

def gerar_especies(especies_base, zonas_info):
    especies_info = []

    for nome_cientifico, nome_comum, categoria in especies_base:
        continente = escolher_continente_para_especie(categoria, zonas_info)

        print(
            f"INSERT INTO especie VALUES "
            f"('{nome_cientifico}', '{nome_comum}', '{categoria}', '{continente}');"
        )

        especies_info.append([nome_cientifico, nome_comum, categoria, continente])

    return especies_info

def sql_texto(valor):
    return "'" + valor.replace("'", "''") + "'"

def zona_compativel_com_especie(zona_info, categoria, continente):
    id_zona, categoria_zona, continente_zona = zona_info

    categoria_ok = categoria_zona == categoria or categoria_zona is None
    continente_ok = continente_zona == continente or continente_zona is None

    return categoria_ok and continente_ok


def recintos_compativeis_com_especie(categoria, continente, zonas_info):
    zonas_compativeis = []

    for zona_info in zonas_info:
        id_zona = zona_info[0]

        if zona_compativel_com_especie(zona_info, categoria, continente):
            zonas_compativeis.append(id_zona)

    recintos_compativeis = []

    for recinto in lista_recintos:
        id_recinto = recinto[0]
        id_zona = recinto[1]

        if id_zona in zonas_compativeis:
            recintos_compativeis.append(id_recinto)

    if len(recintos_compativeis) == 0:
        raise ValueError(f"Não há recinto compatível para {categoria} / {continente}.")

    return recintos_compativeis


def data_nascimento_aleatoria():
    ano = random.randint(1980, 2025)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)

    return f"{ano}-{mes:02d}-{dia:02d}"


def gerar_animais(especies_info, zonas_info):
    ocupacao_recintos={}

    for recinto in lista_recintos:
        id_recinto=recinto[0]
        ocupacao_recintos[id_recinto]=[]

    numero_individual = 1

    for index, especie in enumerate(especies_info):
        nome_cientifico=especie[0]
        nome_comum=especie[1]
        categoria=especie[2]
        continente=especie[3]

        recintos_possiveis=recintos_compativeis_com_especie(
            categoria,
            continente,
            zonas_info
        )

        if index % 10 == 0:
            numero_animais = 1
        else:
            numero_animais = random.choice([2, 3])

        recintos_ocupados_compativeis = []

        for id_recinto in recintos_possiveis:
            if len(ocupacao_recintos[id_recinto]) > 0:
                recintos_ocupados_compativeis.append(id_recinto)

        # De vez em quando tenta pôr espécies diferentes no mesmo recinto.
        if index % 12 == 0 and len(recintos_ocupados_compativeis) > 0:
            id_recinto_escolhido = random.choice(recintos_ocupados_compativeis)
        else:
            recintos_vazios_compativeis = []

            for id_recinto in recintos_possiveis:
                if len(ocupacao_recintos[id_recinto]) == 0:
                    recintos_vazios_compativeis.append(id_recinto)

            if len(recintos_vazios_compativeis) > 0:
                id_recinto_escolhido = random.choice(recintos_vazios_compativeis)
            else:
                id_recinto_escolhido = random.choice(recintos_possiveis)

        for n in range(1, numero_animais + 1):
            nome_animal = f"{nome_comum}_{numero_individual}"
            data_nasc = data_nascimento_aleatoria()

            print(
                "INSERT INTO animal "
                "(id_animal, nome, nome_cientifico, id_recinto, data_nasc) "
                f"VALUES (DEFAULT, {sql_texto(nome_animal)}, {sql_texto(nome_cientifico)}, "
                f"{id_recinto_escolhido}, DATE '{data_nasc}');"
            )

            ocupacao_recintos[id_recinto_escolhido].append(nome_cientifico)
            numero_individual += 1

    return ocupacao_recintos

dias_hash = [None, 32, 29, 32, 31, 32, 12]
MIN_BILHETES_FIM_SEMANA = 4000
MIN_BILHETES_DIA_UTIL = 1000
PERCENTAGEM_BILHETES_TODAS_ZONAS = 2
PROBABILIDADE_NOVA_VENDA = 0.66
PROBABILIDADE_VOTO = 0.9
PROBABILIDADE_DESCONTO = 1 / 3

def hora_aleatoria():
    hora = random.randint(0,23)
    min = random.randint(0,59)
    return f"{hora:02d}:{min:02d}"



def adicionar_venda(vendas_values, no_venda, data):
    nif = int(100000000 + random.random() * 899999999)
    vendas_values.append(
        f"({no_venda}, TIMESTAMP '{data} {hora_aleatoria()}', '{nif}')"
    )


def talvez_proxima_venda(no_venda_atual, data, vendas_values):
    if random.random() < PROBABILIDADE_NOVA_VENDA:
        no_venda_atual += 1
        adicionar_venda(vendas_values, no_venda_atual, data)

    return no_venda_atual


def imprimir_insert(nome_tabela, values):
    if len(values) > 0:
        print(f"INSERT INTO {nome_tabela} VALUES")
        print(",\n".join(values) + ";")


def gerar_combinacoes_obrigatorias(zonas, bilhete_serial, no_venda):
    data_inicial = "2026-01-01"

    vendas_values = []
    bilhetes_values = []
    acesso_values = []

    adicionar_venda(vendas_values, no_venda, data_inicial)

    for mascara in range(1, 2 ** len(zonas)):
        escolhidas = []

        for i in range(len(zonas)):
            if mascara & (1 << i):
                escolhidas.append(zonas[i])

        if len(escolhidas) >= 3:
            bilhetes_values.append(
                f"({bilhete_serial}, DEFAULT, DEFAULT, {no_venda})"
            )

            for id_zona in escolhidas:
                acesso_values.append(
                    f"({bilhete_serial}, {id_zona})"
                )

            bilhete_serial += 1

            if mascara != 2 ** len(zonas) - 1:
                no_venda = talvez_proxima_venda(
                    no_venda,
                    data_inicial,
                    vendas_values
                )

    imprimir_insert("venda", vendas_values)
    imprimir_insert("bilhete", bilhetes_values)
    imprimir_insert("acesso", acesso_values)

    return no_venda, bilhete_serial

def gerar_bilhetes():
    total_votos = 0
    total_days = 0
    bilhete_serial = 1
    no_venda = 1
    zonas = list(range(1, NUM_ZONAS + 1))

    no_venda, bilhete_serial = gerar_combinacoes_obrigatorias(
        zonas,
        bilhete_serial,
        no_venda
    )

    for mes in range(1, 7):
        dias = dias_hash[mes]

        for dia in range(1, dias):
            total_days += 1
            data = f"2026-{mes:02d}-{dia:02d}"

            vendas_values = []
            bilhetes_values = []
            acesso_values = []

            # Garante que cada dia começa com pelo menos uma venda desse dia.
            no_venda += 1
            adicionar_venda(vendas_values, no_venda, data)

            if total_days % 7 == 3 or total_days % 7 == 4:
                bilhetesdiarios = round(
                    MIN_BILHETES_FIM_SEMANA
                    + random.random() * MIN_BILHETES_FIM_SEMANA / 2
                )
            else:
                bilhetesdiarios = round(
                    MIN_BILHETES_DIA_UTIL
                    + random.random() * MIN_BILHETES_DIA_UTIL / 2
                )

            acesso_total = int(
                bilhetesdiarios * PERCENTAGEM_BILHETES_TODAS_ZONAS / 100
            ) + 1

            for bilhete in range(1, bilhetesdiarios + 1):
                desconto = (
                    0.50
                    if random.random() < PROBABILIDADE_DESCONTO
                    else "DEFAULT"
                )

                votou = (
                    "TRUE"
                    if random.random() < PROBABILIDADE_VOTO
                    else "DEFAULT"
                )

                if votou == "TRUE":
                    total_votos += 1

                bilhetes_values.append(
                    f"({bilhete_serial}, {desconto}, {votou}, {no_venda})"
                )

                if bilhete <= acesso_total:
                    for id_zona in zonas:
                        acesso_values.append(
                            f"({bilhete_serial}, {id_zona})"
                        )

                    if votou == "TRUE":
                        votar_em_recinto([], total_votos)

                else:
                    zonas_disponiveis = zonas.copy()
                    numero_de_zonas_acessadas = random.randint(
                        3,
                        len(zonas_disponiveis)
                    )

                    for _ in range(numero_de_zonas_acessadas):
                        id_zona = zonas_disponiveis.pop(
                            random.randint(0, len(zonas_disponiveis) - 1)
                        )

                        acesso_values.append(
                            f"({bilhete_serial}, {id_zona})"
                        )

                    if votou == "TRUE":
                        votar_em_recinto(zonas_disponiveis, total_votos)

                bilhete_serial += 1

                if bilhete != bilhetesdiarios:
                    no_venda = talvez_proxima_venda(
                        no_venda,
                        data,
                        vendas_values
                    )

            imprimir_insert("venda", vendas_values)
            imprimir_insert("bilhete", bilhetes_values)
            imprimir_insert("acesso", acesso_values)

    return total_votos


print("BEGIN;")
zonas_info=gerar_zonas(types, continents)
especies_info=gerar_especies(especies_base, zonas_info)
lista_recintos=gerar_recintos()
ocupacao_recintos=gerar_animais(especies_info, zonas_info)
total_votos=gerar_bilhetes()
atualizar_votos_recintos(total_votos)
print("COMMIT;")