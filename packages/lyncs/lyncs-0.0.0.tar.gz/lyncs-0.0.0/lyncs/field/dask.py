class DaskField(ArrayField):
    @tunable_property
    def chunks(self):
        ChunksOf({key: val for key, val in self.shape if key in self.dims and val > 1})

    @compute_property
    def num_workers(self):
        num_workers = 1
        for num, den in zip(shape, chunks):
            num_workers *= ceil(num / den)

        return num_workers
