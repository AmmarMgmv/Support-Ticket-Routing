import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    className="Navbar",
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Search", href="/search")),
        dbc.NavItem(dbc.NavLink("Admin", href="/admin")),
        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
    ],
    brand="Millennium Management",
    brand_href="/",
    color="#054b80",
    dark=True,
    fluid=True,
    sticky=True,
    links_left=True,
    # style={'font-size':'1.1rem'},
    # brand_style={'font-size':'1.3rem'}
)