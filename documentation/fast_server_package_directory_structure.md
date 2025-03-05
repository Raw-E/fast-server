Directory structure in: /Users/Raw-E/Desktop/Useful Python Things/My Packages/Fast Server
Generated on March 04, 2025 at 08:23:13 PM 

[configurations/]
    - coding-guru-configuration.json
[documentation/]
    - fast_server_package_directory_structure.md
[source_code/]
    [fast_server/]
        - __init__.py
        [v1/]
            - __init__.py
            [api_operation_framework/]
                [api_operation_dependencies/]
                    - log_request_data.py
                - http_methods.py
                [operations/]
                    - api_operation.py
                    - initialize_and_register_api_operations.py
            [services/]
                [server/]
                    - server_configuration.py
                    - server_lifecycle.py
                    - server_runner.py
            [test/]
                [api_operations/]
                    - get_health.py
                    - save_idea.py
                [data_model_handlers/]
                    - idea_data_model_handler.py
                [data_models/]
                    - idea_data_model.py
            [utilities/]
                - __init__.py
                - api_operations_path.py
                - get_user_id_with_authentication_header.py
                - logging_presentation.py
                - logging_related.py
                - port_related.py
[tests/]
    - quick_test.py
    - test_importing_this_package.py
