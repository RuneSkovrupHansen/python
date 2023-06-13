from dataclasses import dataclass

@dataclass
class Inch:
    value: float

@dataclass
class Guitar:
    brand: str
    model: str
    fretboard_radius: Inch
    price: float


def main():
    strandberg_guitar = Guitar(brand="Strandberg*", model="Standard", fretboard_radius=Inch(20), price=1850)

    gibson_guitar = Guitar(brand="Gibson", model="Les Paul Classic TC LH", fretboard_radius=Inch(12), price=1900)

    print(f"strandberg: {strandberg_guitar}")
    print(f"gibson: {gibson_guitar}")

    print(f"equality: {strandberg_guitar == gibson_guitar}")


if __name__ == "__main__":
    main()


