from notion_client_wrapper.properties.property import Property


class FilterBuilder:
    @staticmethod
    def single_equal(property: Property) -> dict:
        return {
            "property": property.name,
            property.type: {
                "equals": property.value_for_filter(),
            },
        }
