import autofit as af


class PipelineDataset(af.Pipeline):
    def run(self, dataset, mask, info=None, pickle_files=None):
        def runner(phase, results):
            return phase.run(
                dataset=dataset,
                results=results,
                mask=mask,
                info=info,
                pickle_files=pickle_files,
            )

        return self.run_function(runner)


class PipelinePositions(af.Pipeline):
    def run(self, positions, pixel_scales):
        def runner(phase, results):
            return phase.run(
                positions=positions, pixel_scales=pixel_scales, results=results
            )

        return self.run_function(runner)
