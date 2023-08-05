from autoconf import conf
import autofit as af
from autoarray.inversion import pixelizations as pix
from autoarray.inversion import regularization as reg
from autogalaxy.hyper import hyper_data as hd
from astropy import cosmology as cosmo
from autofit.tools.phase import Dataset
from autogalaxy.pipeline.phase import abstract
from autogalaxy.pipeline.phase import extensions
from autogalaxy.pipeline.phase.dataset.result import Result

import shutil
import os

class PhaseDataset(abstract.AbstractPhase):
    galaxies = af.PhaseProperty("galaxies")

    Result = Result

    @af.convert_paths
    def __init__(
        self, paths, settings, search, galaxies=None, cosmology=cosmo.Planck15
    ):
        """

        A phase in an lens pipeline. Uses the set non_linear search to try to fit models and hyper_galaxies
        passed to it.

        Parameters
        ----------
        search: class
            The class of a non_linear search
        """

        super().__init__(
            paths,
            search=search,
            settings=settings,
            galaxies=galaxies,
            cosmology=cosmology,
        )

        self.hyper_name = None
        self.use_as_hyper_dataset = False
        self.is_hyper_phase = False

    def run(self, dataset: Dataset, mask, results=None, info=None, pickle_files=None):
        """
        Run this phase.

        Parameters
        ----------
        mask: Mask
            The default masks passed in by the pipeline
        results: autofit.tools.pipeline.ResultsCollection
            An object describing the results of the last phase or None if no phase has been executed
        dataset: scaled_array.ScaledSquarePixelArray
            An masked_imaging that has been masked

        Returns
        -------
        result: AbstractPhase.Result
            A result object comprising the best fit model and other hyper_galaxies.
        """

        self.model = self.model.populate(results)

        results = results or af.ResultsCollection()

        self.modify_dataset(dataset=dataset, results=results)
        self.modify_settings(dataset=dataset, results=results)
        self.modify_search_paths()

        analysis = self.make_analysis(dataset=dataset, mask=mask, results=results)

        self.save_metadata(dataset=dataset)
        self.save_dataset(dataset=dataset)
        self.save_mask(mask=mask)
        self.save_settings(settings=self.settings)
        phase_attributes = self.make_phase_attributes(analysis=analysis)
        self.save_phase_attributes(phase_attributes=phase_attributes)

        result = self.run_analysis(
            analysis=analysis, info=info, pickle_files=pickle_files
        )

        return self.make_result(result=result, analysis=analysis)

    def make_analysis(self, dataset, mask, results=None):
        """
        Create an lens object. Also calls the prior passing and masked_imaging modifying functions to allow child
        classes to change the behaviour of the phase.

        Parameters
        ----------
        mask: Mask
            The default masks passed in by the pipeline
        dataset: im.Imaging
            An masked_imaging that has been masked
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens : Analysis
            An lens object that the non-linear search calls to determine the fit of a set of values
        """
        raise NotImplementedError()

    def modify_dataset(self, dataset, results):
        pass

    def modify_settings(self, dataset, results):
        pass

    def modify_search_paths(self):

        if self.hyper_name is None:
            hyper_tag = ""
        else:
            hyper_tag = f"{self.hyper_name}__"

        if not self.has_pixelization:
            self.search.paths.tag = f"{hyper_tag}{self.settings.phase_tag_no_inversion}"
        else:
            self.search.paths.tag = (
                f"{hyper_tag}{self.settings.phase_tag_with_inversion}"
            )

        output_path = self.search.paths.output_path

        if self.settings.settings_lens.positions_threshold is not None:

            path_containing_settings = output_path.rsplit("/", 1)[0]
            path_containing_settings = path_containing_settings.rsplit("/", 1)[0]

            folders = os.listdir(path_containing_settings)
            folders_to_rename = list(filter(None, [folder if ("pos_on" not in folder) and ("pos" in folder) else None for folder in folders]))

            if len(folders_to_rename) == 0:
                return

            if hyper_tag == "":
                folder_to_rename = folders_to_rename[0]
            else:
                folder_to_rename = [folder for folder in folders_to_rename if hyper_tag in folder][0]

            shutil.rmtree(f"{path_containing_settings}/{self.search.paths.tag}")
            os.rename(
                f"{path_containing_settings}/{folder_to_rename}",
                f"{path_containing_settings}/{self.search.paths.tag}"
            )


    def extend_with_inversion_phase(self, inversion_search):
        return extensions.InversionPhase(
            phase=self,
            search=inversion_search,
            model_classes=(pix.Pixelization, reg.Regularization),
        )

    def extend_with_multiple_hyper_phases(self, setup_hyper, include_inversion=False):

        self.use_as_hyper_dataset = True

        hyper_phases = []

        if include_inversion:
            if self.has_pixelization and setup_hyper.inversion_search:

                if (
                    not setup_hyper.hyper_image_sky
                    and not setup_hyper.hyper_background_noise
                ):
                    phase_inversion = extensions.InversionPhase(
                        phase=self,
                        search=setup_hyper.inversion_search,
                        model_classes=(pix.Pixelization, reg.Regularization),
                    )
                elif (
                    setup_hyper.hyper_image_sky
                    and not setup_hyper.hyper_background_noise
                ):
                    phase_inversion = extensions.InversionPhase(
                        phase=self,
                        search=setup_hyper.inversion_search,
                        model_classes=(
                            pix.Pixelization,
                            reg.Regularization,
                            hd.HyperImageSky,
                        ),
                    )
                elif (
                    not setup_hyper.hyper_image_sky
                    and setup_hyper.hyper_background_noise
                ):
                    phase_inversion = extensions.InversionPhase(
                        phase=self,
                        search=setup_hyper.inversion_search,
                        model_classes=(
                            pix.Pixelization,
                            reg.Regularization,
                            hd.HyperBackgroundNoise,
                        ),
                    )
                else:
                    phase_inversion = extensions.InversionPhase(
                        phase=self,
                        search=setup_hyper.inversion_search,
                        model_classes=(
                            pix.Pixelization,
                            reg.Regularization,
                            hd.HyperImageSky,
                            hd.HyperBackgroundNoise,
                        ),
                    )

                hyper_phases.append(phase_inversion)

        if setup_hyper.hyper_galaxies_search is not None:
            phase_hyper_galaxy = extensions.HyperGalaxyPhase(
                phase=self,
                search=setup_hyper.hyper_galaxies_search,
                include_sky_background=setup_hyper.hyper_image_sky,
                include_noise_background=setup_hyper.hyper_background_noise,
                hyper_galaxy_names=setup_hyper.hyper_galaxy_names,
            )
            hyper_phases.append(phase_hyper_galaxy)

        if setup_hyper.hyper_galaxy_phase_first:
            if (
                include_inversion and setup_hyper.inversion_search is not None
            ) and setup_hyper.hyper_galaxies_search is not None:
                hyper_phases = [phase for phase in reversed(hyper_phases)]

        if len(hyper_phases) == 0:
            return self
        else:
            return extensions.CombinedHyperPhase(
                phase=self,
                search=setup_hyper.hyper_combined_search,
                hyper_phases=hyper_phases,
            )
