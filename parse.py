from pyparsing import Word, Literal, QuotedString, Group, Suppress, nums, OneOrMore, Optional

# Définition des éléments de base du langage
LBRACE, RBRACE, EQ, SEMICOLON = map(Suppress, '{}=;')
ARROW = Suppress(Literal("->"))
quoted_string = QuotedString('"', esc_char='\\')
number = Word(nums).set_parse_action(lambda t: int(t[0]))

# Définition de l'expression de taille optionnelle
optional_size = Optional(Suppress(Literal("size")) + EQ + number.set_results_name("size") + SEMICOLON)

# Définition de l'expression de couleur optionnelle
optional_packet_color = Optional(Suppress(Literal("packet_color")) + EQ + number.set_results_name("packet_color") + SEMICOLON)

optional_child = Optional(ARROW + quoted_string.set_results_name("child"))


# Définition d'un champ avec une taille optionnelle
field_def = Group(
    Suppress(Literal("field")) +
    quoted_string.set_results_name("field_name") + LBRACE +
    optional_size + RBRACE + optional_child
)

# Définition d'un paquet
packet_def = Group(
    Suppress(Literal("packet")) +
    quoted_string.set_results_name("packet_name") + LBRACE +
    optional_packet_color +
    OneOrMore(field_def).set_results_name("fields") + RBRACE
)

# On peut définir le parser final
full_parser = OneOrMore(packet_def)

text_to_parse = """
packet "Packet1" {
    field "SOF (3 bits)" {
        size = 5;
    }
    field "CAN ID (11 bits)" {
        size = 11;
    } -> "Packet2"
}
packet "Packet2" {
    field "DLC (4 bits)" {
        size = 4;
    }
}
"""

try:
    results = full_parser.parse_string(text_to_parse)

    # Convertir les résultats en une liste de dictionnaires
    parsed_data = [result.as_dict() for result in results]
    
    # Afficher les résultats structurés
    print(parsed_data)

except Exception as e:
    print(f"Erreur d'analyse: {e}")