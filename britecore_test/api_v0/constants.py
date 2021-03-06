DEFAULT_SCHEMA_ITEM_KEYS = [
    'field_id',
    'field_name',
    'field_type',
    'options',
    'optionDisabled',
    'is_required',
]
SCHEMA_ITEM_KEYS_UPDATE_1 = DEFAULT_SCHEMA_ITEM_KEYS + ['value']
SCHEMA_ITEM_KEYS_UPDATE_2 = SCHEMA_ITEM_KEYS_UPDATE_1 + ['generatedOptions']
TEST_SCHEMA = [
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "first_name",
        "field_type": "text",
        "is_required": True,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "email",
        "field_type": "email",
        "is_required": True,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "phone",
        "field_type": "tel",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "b_date",
        "field_type": "date",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "b_time",
        "field_type": "time",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "doc",
        "field_type": "file",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "instagram_link",
        "field_type": "url",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": [11, 89],
        "options": "10, 90",
        "field_name": "lucky_numbers",
        "field_type": "range",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "10",
                "value": 10
            },
            {
                "text": "90",
                "value": 90
            }
        ]
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "best_number",
        "field_type": "number",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": None,
        "value": None,
        "options": "traveling, "
                   "cooking, "
                   "dancing",
        "field_name": "hobbies",
        "field_type": "checkbox",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "traveling",
                "value": False
            },
            {
                "text": "cooking",
                "value": False
            },
            {
                "text": "dancing",
                "value": False
            }
        ]
    },
    {
        "field_id": None,
        "value": None,
        "options": "no_bad_habbits, "
                   "smoking, "
                   "smth_else",
        "field_name": "bad_habbits",
        "field_type": "radio",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "no_bad_habbits",
                "value": 0
            },
            {
                "text": "smoking",
                "value": 1
            },
            {
                "text": "smth_else",
                "value": 2
            }
        ]
    },
    {
        "field_id": None,
        "value": None,
        "options": "Mar, Apr, May",
        "field_name": "desired_month",
        "field_type": "select",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "Mar",
                "value": 0
            },
            {
                "text": "Apr",
                "value": 1
            },
            {
                "text": "May",
                "value": 2
            }
        ]
    },
    {
        "field_id": None,
        "value": None,
        "options": "",
        "field_name": "description",
        "field_type": "textarea",
        "is_required": False,
        "optionDisabled": True
    }
]

TEST_RISK_DATA = [
    {
        "field_id": 1,
        "value": "Dmitry",
        "options": "",
        "field_name": "first_name",
        "field_type": "text",
        "is_required": True,
        "optionDisabled": True
    },
    {
        "field_id": 2,
        "value": "danilovdmitry94@gmail.com",
        "options": "",
        "field_name": "email",
        "field_type": "email",
        "is_required": True,
        "optionDisabled": True
    },
    {
        "field_id": 3,
        "value": "0932812462",
        "options": "",
        "field_name": "phone",
        "field_type": "tel",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 4,
        "value": "1994-04-24",
        "options": "",
        "field_name": "b_date",
        "field_type": "date",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 5,
        "value": "20:00",
        "options": "",
        "field_name": "b_time",
        "field_type": "time",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 6,
        "value": None,
        "options": "",
        "field_name": "doc",
        "field_type": "file",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 7,
        "value": "https://www.instagram.com/______dmitry/",
        "options": "",
        "field_name": "instagram_link",
        "field_type": "url",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 8,
        "value": [11, 89],
        "options": "10, 90",
        "field_name": "lucky_numbers",
        "field_type": "range",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "10",
                "value": 10
            },
            {
                "text": "90",
                "value": 90
            }
        ]
    },
    {
        "field_id": 9,
        "value": "6",
        "options": "",
        "field_name": "best_number",
        "field_type": "number",
        "is_required": False,
        "optionDisabled": True
    },
    {
        "field_id": 10,
        "value": None,
        "options": "traveling, cooking, dancing",
        "field_name": "hobbies",
        "field_type": "checkbox",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "traveling",
                "value": True
            },
            {
                "text": "cooking",
                "value": True
            },
            {
                "text": "dancing",
                "value": False
            }
        ]
    },
    {
        "field_id": 11,
        "value": 0,
        "options": "no_bad_habbits, smoking, smth_else",
        "field_name": "bad_habbits",
        "field_type": "radio",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "no_bad_habbits",
                "value": 0
            },
            {
                "text": "smoking",
                "value": 1
            },
            {
                "text": "smth_else",
                "value": 2
            }
        ]
    },
    {
        "field_id": 12,
        "value": 0,
        "options": "Mar, Apr, May",
        "field_name": "desired_month",
        "field_type": "select",
        "is_required": False,
        "optionDisabled": False,
        "generatedOptions": [
            {
                "text": "Mar",
                "value": 0
            },
            {
                "text": "Apr",
                "value": 1
            },
            {
                "text": "May",
                "value": 2
            }
        ]
    },
    {
        "field_id": 13,
        "value": "Lorem Ipsum is simply dummy text of the printing and...",
        "options": "",
        "field_name": "description",
        "field_type": "textarea",
        "is_required": False,
        "optionDisabled": True
    }
]
