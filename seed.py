from app import app, db, SiteContent, Skill, Experience, Project, Education

def seed_data():
    with app.app_context():
        db.create_all()

        # Check if already seeded
        if Skill.query.first() is not None:
            print("Database already seeded.")
            return

        # Seed SiteContent
        site_content = SiteContent(
            hero_title="Hi, I'm Pranav Sahu",
            hero_subtitle="Full-Stack Developer,Software Engineer,Robotics Enthusiast,Creative Coder,Problem Solver",
            hero_description="I build innovative and efficient web applications. Passionate about clean code, user experience, and cutting-edge technologies.",
            about_text="Hello! I'm Pranav, a developer with a knack for creating dynamic and responsive web applications. My journey into tech started with a fascination for how things work, which quickly evolved into a passion for building software that solves real-world problems.\n\nWith a strong foundation in both front-end and back-end development, I enjoy the entire process of bringing an idea to life, from initial concept to deployment. I'm a lifelong learner, always eager to explore new technologies and improve my skill set.\n\nWhen I'm not coding, you can find me exploring IoT technologies, ricing linux, or contributing to open-source projects.",
            about_image_path="my_prof_pic.jpg",
            resume_file_path="#"
        )
        db.session.add(site_content)

        # Seed Education
        ed1 = Education(
            display_order=10,
            period="2021 - 2023",
            degree="Higher Secondary Education",
            institution="KPS Raipur",
            description="Completed my higher secondary education, scoring 89%, with a strong foundation in mathematics, physics, and computer science."
        )
        ed2 = Education(
            display_order=20,
            period="2024 - Present",
            degree="B.Tech in Computer Science and Engineering",
            institution="Amity University Rajasthan",
            description="Currently in 2nd year, maintaining a strong academic record while actively participating in coding and robotics competitions."
        )
        db.session.add_all([ed1, ed2])

        # Seed Skills
        skills = [
            ("Python", "code-2"),
            ("C", "hash"),
            ("C++", "plus"),
            ("JavaScript", "file-json-2"),
            ("Node.js", "box"),
            ("MySQL", "database"),
            ("Flask", "flask-conical"),
            ("Linux", "terminal"),
            ("Git & GitHub", "git-branch"),
            ("Arduino", "cpu")
        ]
        for name, icon in skills:
            db.session.add(Skill(name=name, icon_class=icon))

        # Seed Experiences
        exp1 = Experience(
            display_order=10,
            period="July 2025 - Present",
            title="Senior Developer at RAIoT Club",
            company="RAIoT Club",
            description="Senior Developer at the Club, building real world projects based on robotics and latest technologies.",
            image_path="iitr_me2.jpg"
        )
        exp2 = Experience(
            display_order=20,
            period="March 2025",
            title="Cognizance IIT Roorkee",
            company="Cognizance",
            description="Team Leader for Line Follower competition, and Improvised the logic of the bot for better results. Helped the team in various other technical events and hackathons.",
            image_path="iitr.jpg"
        )
        exp3 = Experience(
            display_order=30,
            period="January 2025",
            title="Prometeo IIT Jodhpur",
            company="Prometeo",
            description="Led my team in Line Follower competition, Web-Hackathon and Capture-The-Flag event. Implemented embedded programming in various robotics events.",
            image_path="20250120_020853.jpg"
        )
        exp4 = Experience(
            display_order=40,
            period="November 2024",
            title="Sphinx MNIT",
            company="Sphinx",
            description="Participated in aero-modeling competition, and various other robotics events.",
            image_path="sphinx.jpg"
        )
        exp5 = Experience(
            display_order=50,
            period="Sept 2024 - Mar 2025",
            title="Junior Developer at RAIoT Club",
            company="RAIoT Club",
            description="Worked on various projects related to IoT and robotics, using various technologies like Arduino, ESP32, etc.",
            image_path="raiot-logo.jpeg"
        )
        db.session.add_all([exp1, exp2, exp3, exp4, exp5])

        # Seed Projects
        p1 = Project(
            display_order=10,
            title="Attendance System",
            description="A full-featured IoT-based attendance solution that combines a physical check-in device with a powerful web-based backend. A person can clock in using an RFID card or a PIN on a numpad, with an LCD for instant feedback. The system features a Django web portal for administration and seamlessly syncs all attendance data in real-time directly to a Google Sheet, making record-keeping simple and accessible.",
            tags="ESP,Python,Django,Google Sheets API",
            image_path="rfid.jpeg",
            github_link="#",
            external_link="#"
        )
        p2 = Project(
            display_order=20,
            title="Line Follower Bot",
            description="An Arduino-based robot using a PID algorithm and an IR sensor array for ultra-smooth line following. It also implements a maze-solving algorithm to autonomously navigate complex intersections and paths. A TB6 motor driver provides precise motor control.",
            tags="Arduino,IOT,C++",
            image_path="line-follower.jpg",
            github_link="#",
            external_link="#"
        )
        p3 = Project(
            display_order=30,
            title="Portfolio Website",
            description="A minimalist developer portfolio built from scratch with vanilla HTML, CSS, and JavaScript. It features a dynamic particle animation background and subtle interactive effects to create a clean, modern, and engaging user experience.",
            tags="HTML,CSS,JavaScript",
            image_path="Portfolio-Desenvolvedor-Web.webp",
            github_link="#",
            external_link="#"
        )
        db.session.add_all([p1, p2, p3])

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
