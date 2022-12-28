import jinja2

attendees = [
    "Marco",
    "Jackson",
    "Emily Whelan",
    "Misha",
    "Henry",
    "Katherine",
    "Matt",
    "Callum",
    "Chris",
    "Emily Doyle",
    "Rosie",
]


def main():

    # Set up the Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates/")
    template_env = jinja2.Environment(loader=template_loader)

    # Load the template
    template = template_env.get_template("clue.html")

    # Define the template context
    context = {
        "teams": [
            {
                "id": 1,
                "name": "Team A",
                "description": "This is the description for Team A.",
            },
            {
                "id": 2,
                "name": "Team B",
                "description": "This is the description for Team B.",
            },
            {
                "id": 3,
                "name": "Team C",
                "description": "This is the description for Team C.",
            },
        ]
    }

    # Render the template with the context
    output = template.render(context)

    # Print the output to the console
    print(output)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
