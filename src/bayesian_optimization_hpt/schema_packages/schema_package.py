from typing import (
    TYPE_CHECKING,
)

from nomad.config import config
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections import (
    ActivityStep,
    Measurement,
    MeasurementResult,
    SectionReference,
)
from nomad.metainfo import (
    MEnum,
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)
from nomad.parsing.tabular import TableData
from nomad_analysis.general.schema import AnalysisStep
from nomad_analysis.jupyter.schema import ELNJupyterAnalysis

if TYPE_CHECKING:
    pass

configuration = config.get_plugin_entry_point(
    'bayesian_optimization_hpt.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class PassivationPerformanceResult(MeasurementResult):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    carrier_lifetime = Quantity(
        type=float,
        description='The average time taken for a carrier to recombine.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'microsecond'},
        a_tabular={'name': 'Carrier lifetime [um]'},
        unit='microsecond',
    )


class HydrogenPlasmaTreatment(ActivityStep):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=['comment']),
                order=[
                    'name',
                    'datetime',
                ],
            )
        )
    )
    temperature = Quantity(
        type=float,
        description='Process temperature.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'K'},
        a_tabular={'name': 'Process temperature [K]'},
        unit='kelvin',
    )
    duration = Quantity(
        type=float,
        description='Process duration.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'minute'},
        a_tabular={'name': 'Process time [min]'},
        unit='minute',
    )
    h2_pressure = Quantity(
        type=float,
        description='Hydrogen gas pressure.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'Pa'},
        a_tabular={'name': 'H2 pressure [Pa]'},
        unit='Pa',
    )
    h2_flow_rate = Quantity(
        type=float,
        description='Hydrogen gas flow rate.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'cm**3/minute'},
        a_tabular={'name': 'H2 flow rate [sccm]'},
        unit='cm**3/minute',
    )
    rf_power = Quantity(
        type=float,
        description="""
        RF (radio frequency) power supplied to generate and sustain plasma.
        """,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'W'},
        a_tabular={'name': 'RF power [W]'},
        unit='W',
    )
    electrode_distance = Quantity(
        type=float,
        description='Distance between electrodes.',
        a_eln={
            'component': 'NumberEditQuantity',
            'defaultDisplayUnit': 'millimeter',
        },
        a_tabular={'name': 'Electrod distance [mm]'},
        unit='millimeter',
    )


class PassivationPerformanceMeasurement(Measurement, EntryData):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section(
        more={'label_quantity': '#/data/name'},
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
        a_tabular={'name': 'Experiment name'},
    )
    steps = SubSection(
        section_def=HydrogenPlasmaTreatment,
        repeats=True,
    )
    results = SubSection(
        section_def=PassivationPerformanceResult,
        repeats=True,
    )


class PassivationPerformanceMeasurementReference(SectionReference):
    reference = SectionReference.reference
    reference.type = PassivationPerformanceMeasurement


class HydrogenPlasmaTreatments(ArchiveSection):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    reference = Quantity(
        type=PassivationPerformanceMeasurement,
        a_eln={'component': 'ReferenceEditQuantity'},
    )


class HPTDataLoader(EntryData, TableData):
    """
    Class autogenerated from yaml schema.
    """

    m_def = Section()
    data_file = Quantity(
        type=str,
        a_tabular_parser={
            'mapping_options': [
                {
                    'mapping_mode': 'row',
                    'file_mode': 'multiple_new_entries',
                    'sections': ['hydrogen_plasma_treatments'],
                }
            ]
        },
        a_browser={'adaptor': 'RawFileAdaptor'},
        a_eln={'component': 'FileEditQuantity'},
    )
    hydrogen_plasma_treatments = SubSection(
        section_def=HydrogenPlasmaTreatments,
        repeats=True,
    )


class InitialSampling(AnalysisStep):
    """
    Initial sampling of the data for the Bayesian optimization.
    It contains the samples used for initial training of the surrogate model.
    """

    samples = SubSection(
        section_def=PassivationPerformanceMeasurementReference,
        description='The input sections for the analysis',
        repeats=True,
    )


class MinMaxRange(ArchiveSection):
    """
    Range of a physical quantity.
    """

    name = Quantity(
        type=str,
        description='The name of the physical quantity.',
        a_eln={'component': 'StringEditQuantity'},
    )
    min_value = Quantity(
        type=float,
        description='The minimum value of the physical quantity.',
        a_eln={'component': 'NumberEditQuantity'},
    )
    max_value = Quantity(
        type=float,
        description='The maximum value of the physical quantity.',
        a_eln={'component': 'NumberEditQuantity'},
    )


class MinMaxScaling(AnalysisStep):
    """
    Min-max scaling of the data.
    """

    min_max_ranges = SubSection(
        section_def=MinMaxRange,
        repeats=True,
    )


class Acquisition(AnalysisStep):
    """
    Acquisition of the data for the Bayesian optimization.
    """

    proposal = SubSection(
        section_def=HydrogenPlasmaTreatment,
        description='The proposed process parameters.',
    )
    sample = SubSection(
        section_def=PassivationPerformanceMeasurementReference,
        description='The sample for the data acquisition.',
    )


class SurrogateModel(ArchiveSection):
    """
    Surrogate model for the Bayesian optimization.
    """

    name = Quantity(
        type=str,
        description='The name of the surrogate model.',
        a_eln={'component': 'StringEditQuantity'},
    )
    model_type = Quantity(
        type=MEnum('Gaussian Process'),
        description='The type of the surrogate model taken from sklearn library.',
        a_eln={'component': 'EnumEditQuantity'},
    )
    model_path = Quantity(
        type=str,
        description="""
        Path of the serialized surrogate model taken from sklearn library.
        """,
    )
    description = Quantity(
        type=str,
        description='The description of the surrogate model.',
        a_eln={'component': 'RichTextEditQuantity'},
    )
    trained_on = SubSection(
        section_def=PassivationPerformanceMeasurementReference,
        repeats=True,
    )


class BayesianOptimizationHPT(ELNJupyterAnalysis):
    """
    Bayesian optimization for the hydrogen plasma treatment.
    """

    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=['input_entry_class', 'query_for_inputs']),
                order=[
                    'name',
                    'datetime',
                    'lab_id',
                    'location',
                    'notebook',
                    'reset_notebook',
                    'query_for_inputs',
                    'description',
                    'analysis_type',
                    'surrogate_model',
                ],
            ),
        )
    )
    analysis_type = ELNJupyterAnalysis.analysis_type
    analysis_type.default = 'Bayesian Optimization'

    surrogate_model = SubSection(section_def=SurrogateModel)
    steps = SubSection(section_def=AnalysisStep, repeats=True)

    def normalize(self, archive, logger):
        if self.surrogate_model:
            self.surrogate_model.trained_on = []
            current_optimized_params = None
            for step in self.steps:
                if isinstance(step, InitialSampling):
                    self.surrogate_model.trained_on.extend(step.samples)
                elif isinstance(step, Acquisition):
                    current_optimized_params = step
                    self.surrogate_model.trained_on.append(step.sample)
            if current_optimized_params:
                self.outputs = [current_optimized_params.sample]
        super().normalize(archive, logger)


m_package.__init_metainfo__()
