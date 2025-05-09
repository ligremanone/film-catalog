from schemas.film import Film

FILMS = [
    Film(
        slug="the-shawshank-redemption",
        name="The Shawshank Redemption",
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        year=1994,
        rating=9.3,
    ),
    Film(
        slug="the-godfather",
        name="The Godfather",
        description="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        year=1972,
        rating=9.2,
    ),
    Film(
        slug="the-dark-knight",
        name="The Dark Knight",
        description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one that he can't control.",
        year=2008,
        rating=9.0,
    ),
]
