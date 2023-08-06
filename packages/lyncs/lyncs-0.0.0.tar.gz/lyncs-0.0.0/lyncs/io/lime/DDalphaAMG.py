from ... import DDalphaAMG


def read_chunk(filename, shape, chunks=None, chunk_id=None):
    comm = create_comm()
    procs = np.array(shape) / np.array(chunks)

    solver = DDalphaAMG.Solver(procs=procs, global_lattice=shape[:4])
    return solver.read_configuration
    lib = DDalphaAMG.get_lib()


@computable
def read(filename, shape, chunks):
    from dask.highlevelgraph import HighLevelGraph
    from dask.array.core import normalize_chunks, Array
    from ...mpi.dask_mpi import default_client
    from ...DDalphaAMG import Solver

    client = default_client()
    procs = np.array(shape) / np.array(chunks)
    assert prod(procs[4:]) == 1, "Only space-time dimensions can be parallelized"
    procs = procs[:4]
    assert prod(procs) <= len(DDalphaAMG.available_workers)

    solver = Solver(procs=procs)

    normal_chunks = normalize_chunks(chunks, shape=shape)
    chunk_ids = list(product(*[range(len(bd)) for bd in normal_chunks]))

    reads = [
        delayed(read_chunk)(filename, shape, chunks, chunk_id) for chunk_id in chunks_id
    ]
    keys = [read.key for read in reads]
    client.add

    keys = [(filename, *chunk_id) for chunk_id in chunks_id]
    vals = [read.key for read in reads]
    dsk = dict(zip(keys, vals))

    graph = HighLevelGraph.from_collections(filename, dsk, dependencies=reads)

    return Array(graph, filename, normal_chunks, dtype="complex128")
