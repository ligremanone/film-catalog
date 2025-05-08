from schemas.film import Film

FILMS = [
    Film(
        id=1,
        name="The Shawshank Redemption",
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        year=1994,
        rating=9.3,
    ),
    Film(
        id=2,
        name="The Godfather",
        description="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        year=1972,
        rating=9.2,
    ),
    Film(
        id=3,
        name="The Dark Knight",
        description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one that he can't control.",
        year=2008,
        rating=9.0,
    ),
]
