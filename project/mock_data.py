QUESTIONS = [
    {
        "id": 1,
        "question": "Tkinter does not display Frames correctly after grid_remove() under macOS",
        "answer_count": 5,
        "avatar": 'img/avatarka.png',
        "description_question": """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                                    The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                                    Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                                    mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                                    chances to run on an old osx).""",
        "tags": ["python", "macos", "tkinter"],
    },
    {
        "id": 2,
        "question": "Angular SSR doesn't serve HTML",
        "answer_count": 4,
        "avatar": 'img/avatarka.png',
        "description_question": """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                                    the schematics ng add @angular/ssr which generated the following files:""",
        "tags": ["angular", "angular-ssr", "server-side-rendering"],
    },
    {
        "id": 3,
        "question": "Undefined reference to string constructor with a particular compiler and flags",
        "answer_count": 3,
        "avatar": 'img/avatarka.png',
        "description_question": """The linker error goes away when removing the sanitizer, switching to -O0 (but not -O1),
                                    removing -fconcepts or switching to C++14 or C++20. I can't try to replicate it on Compiler
                                    Explorer since it doesn't have this GCC version yet, but with 15.2.0 this error also goes away -
                                    I assume it's specific to 15.2.1 especially since I haven't encountered it before.
                                    GCC is installed from Arch Linux repos and the linked /usr/lib/libubsan.so.1 is also from those repos,
                                    package gcc-libs 15.2.1 - nothing off there.""",
        "tags": ["c++", "gcc", "compiler-bug"],
    },
    {
        "id": 4,
        "question": "Snowflake undrop temporary table with DATA_RETENTION_TIME_IN_DAYS=0 successful",
        "answer_count": 2,
        "avatar": 'img/avatarka.png',
        "description_question": """I am preparing for the Snowflake exam and tested setting DATA_RETENTION_TIME_IN_DAYS = 0.
                                    This works for permanent tables and transient tables.""",
        "tags": ["snowflake-cloud-data-platform", "snowflake-schema"],
    },
    {
        "id": 5,
        "question": "SwiftData - limit to one of each matching query",
        "answer_count": 1,
        "avatar": 'img/avatarka.png',
        "description_question": """This is, as you likely guessed, an activity log. There are many itemNames.
                                    The "items" generate log entries several times within a date range in unpredictable
                                    intervals and order. I have a SwiftUI view that shows all the logged activity
                                    in a SwiftUI List, including filtering options, and that's all working fine.""",
        "tags": ["swift", "swiftui", "swiftdata"],
    }
]

ANSWERS = [
    {
        "id": 1,
        "avatar": 'img/avatarka.png',
        "description_answer": """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
                                   using the input’s offset() relative to <body> --When the input is inside a position:
                                   sticky container, the input’s visual position changes during scroll, but its offset
                                   relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
                                   events of sticky parents, the popup stays stuck at the original coordinates. We can fix
                                   this by forcing the datepicker to reposition itself whenever its container scrolls.""",
    },
    {
        "id": 2,
        "avatar": 'img/avatarka.png',
        "description_answer": """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
                                   using the input’s offset() relative to <body> --When the input is inside a position:
                                   sticky container, the input’s visual position changes during scroll, but its offset
                                   relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
                                   events of sticky parents, the popup stays stuck at the original coordinates. We can fix
                                   this by forcing the datepicker to reposition itself whenever its container scrolls.""",
    },
    {
        "id": 3,
        "avatar": 'img/avatarka.png',
        "description_answer": """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
                                   using the input’s offset() relative to <body> --When the input is inside a position:
                                   sticky container, the input’s visual position changes during scroll, but its offset
                                   relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
                                   events of sticky parents, the popup stays stuck at the original coordinates. We can fix
                                   this by forcing the datepicker to reposition itself whenever its container scrolls.""",
    },
]

PROFILE_MEMBERS = [
    {
        "id": 1,
        "avatar": 'img/avatarka.png',
        "Questions": [
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """I  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
        "Answers": [
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
    },
    {
        "id": 2,
        "avatar": 'img/avatarka.png',
        "Questions": [
            """You  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
        "Answers": [
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
    },
    {
        "id": 3,
        "avatar": 'img/avatarka.png',
        "Questions": [
            """She  has the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
        "Answers": [
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
    },
    {
        "id": 4,
        "avatar": 'img/avatarka.png',
        "Questions": [
            """He  has the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
        "Answers": [
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
    },
    {
        "id": 5,
        "avatar": 'img/avatarka.png',
        "Questions": [
            """We  have the following problem. I created a desktop application to generate invoices for my dad's company.
                The machine I wrote this application for is an iMac from 2011 running macOS High Sierra (10.13.6).
                Because I have no Mac to test on and the age of the target system, I choose tkinter to implement the GUI
                mainly for its cross-platform compatibility (and because i taught that tkinter is kind of old so it has good
                chances to run on an old osx).""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
        "Answers": [
            """Why it happens --Zebra_DatePicker calculates the popup’s position once when it opens,
               using the input’s offset() relative to <body> --When the input is inside a position:
               sticky container, the input’s visual position changes during scroll, but its offset
               relative to <body> does not change. --Because Zebra_DatePicker doesn’t listen to scroll
               events of sticky parents, the popup stays stuck at the original coordinates. We can fix
               this by forcing the datepicker to reposition itself whenever its container scrolls.""",
            """I added the Angular SSR boilerplate code to my existing Angular 21 project by using
                the schematics ng add @angular/ssr which generated the following files:""",
        ],
    },
]
