import os
from django.core.management.commands.runserver import Command as RunServer


class Command(RunServer):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--no-use-firebase-emulator",
            action="store_false",
            dest="use_firebase_emulator",
            help="Tells Firebase Admin SDK to NOT use emulator.",
        )

    def inner_run(self, *args, **options):
        if options["use_firebase_emulator"]:
            self.stdout.write(
                self.style.WARNING(
                    "start emulators with 'firebase emulators:start'\n"
                    "if you don't intend to use emulators, call django command "
                    "'runserver' with the parameter '--no-use-firebase-emulator'"
                )
            )
            firebase_emulator_vars = {
                "FIREBASE_AUTH_EMULATOR_HOST": "localhost:9099",
                "FIREBASE_DATABASE_EMULATOR_HOST": "localhost:9000",
                "FIRESTORE_EMULATOR_HOST": "localhost:8080",
                "PUBSUB_EMULATOR_HOST": "localhost:8085",
            }
            for env_name in firebase_emulator_vars:
                os.environ.setdefault(env_name, firebase_emulator_vars[env_name])
                self.stdout.write(
                    self.style.WARNING(
                        "- environment variable {env_name} set to {env_value}".format(
                            env_name=env_name,
                            env_value=firebase_emulator_vars[env_name],
                        )
                    )
                )
        super().inner_run(*args, **options)
