from nomad.config.models.plugins import ExampleUploadEntryPoint

example_upload_entry_point = ExampleUploadEntryPoint(
    title='Bayesian Optimization HPT Example Upload',
    category='Examples',
    description="""
    This example upload demonstrates how to use the Bayesian Optimization HPT schema
    package to train a surrogate model with initial samples and generate proposals for
    new acquisition.
    """,
    path='example_uploads/getting_started',
)
