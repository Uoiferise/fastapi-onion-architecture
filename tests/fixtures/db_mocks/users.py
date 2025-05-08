from uuid import UUID

USERS = (
    # users from first company
    {
        'id': UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'middle_name': 'Ivanovich',
        'company_id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
    },
    {
        'id': UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
        'first_name': 'Elon',
        'last_name': 'Musk',
        'middle_name': None,
        'company_id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
    },
    {
        'id': UUID('d5621653-f72b-4124-98e6-79c5d9c2dc2b'),
        'first_name': 'Ivan',
        'last_name': 'Terrible',
        'middle_name': 'Vasilievich',
        'company_id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
    },

    # users from second company
    {
        'id': UUID('4289fdd9-9fd3-4f39-a10b-a703a4fd23f0'),
        'first_name': 'Ivan',
        'last_name': 'Second',
        'middle_name': 'Company',
        'company_id': UUID('9aff97eb-8b16-47d8-8ddc-dcdadb286d61'),
    },
)
