export interface ContestCard {
    end_registration: string,
    name: string,
    author: string,
    participants: number,
    about_text: string,
    picture_path: string,
}

export let debug_cards: ContestCard[] = [
    {
        author: 'bokisarik',
        end_registration: "December the 27",
        name: "Pre New Year Programming Contest",
        participants: 1283,
        about_text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus proin nibh nisl condimentum id. Tincidunt augue interdum velit euismod. Viverra nam libero justo laoreet sit. Enim nunc faucibus a pellentesque sit. Viverra justo nec ultrices dui. Adipiscing elit ut aliquam purus sit. Tellus pellentesque eu tincidunt tortor. Cursus metus aliquam eleifend mi. Etiam tempor orci eu lobortis. Est placerat in egestas erat imperdiet. Elementum tempus egestas sed sed risus pretium quam vulputate. Diam sollicitudin tempor id eu nisl nunc. Felis donec et odio pellentesque. Pharetra et ultrices neque ornare. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet.',
        picture_path: 'assets/background_svgs/contest_backgrounds/img.png',
    },
    {
        author: 'physicus',
        end_registration: "December the 27",
        name: "Pre New Year Programming Contest",
        participants: 1283,
        about_text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus proin nibh nisl condimentum id. Tincidunt augue interdum velit euismod. Viverra nam libero justo laoreet sit. Enim nunc faucibus a pellentesque sit. Viverra justo nec ultrices dui. Adipiscing elit ut aliquam purus sit. Tellus pellentesque eu tincidunt tortor. Cursus metus aliquam eleifend mi. Etiam tempor orci eu lobortis. Est placerat in egestas erat imperdiet. Elementum tempus egestas sed sed risus pretium quam vulputate. Diam sollicitudin tempor id eu nisl nunc. Felis donec et odio pellentesque. Pharetra et ultrices neque ornare. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet.',
        picture_path: 'assets/background_svgs/contest_backgrounds/img.png',
    },
]