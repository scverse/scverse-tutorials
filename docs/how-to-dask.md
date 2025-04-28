# Dask Q&A

Here we will go through some common questions and answers about `dask`, with a special focus on its integration with `scanpy` and `anndata`.

## Quickstart

**How do I monitor the {doc}`dask dashboard <dask:dashboard>`?**

If you are in a jupyter notebook, when you render the `repr` of your `client`, you will see a link, usually something like `http://localhost:8787/status`.
If you are working locally, this link alone should suffice.

If you are working on some sort of remote notebook from a web browser, you will need to replace `http://localhost:8787` by the root url of the notebook.

If you are in vscode, there is an [`dask` extension] which will allow you to monitor there.

**How do I know how to allocate resources?**

In `dask`, every worker will receive an equal share of the memory available.
So if you request e.g., a slurm job with 256GB of RAM, and then start 8 workers, each will have 32 GB of memory.

`dask` distributes jobs to each worker generally based on the chunking of the array.
So if you have dense chunks of `(30_000, 30_000)` with 32 bit integers, you will need to be have 3.6 GB for each worker, at the minimum to even load the data.
Then if you do something like matrix multiplication, you will need double or even more, as an example.

**How do I read my data into a `dask` array?**

{func}`anndata.experimental.read_elem_lazy` or {func}`anndata.experimental.read_lazy` can help you if you already have data on-disk that was written to the `anndata` file format.
If you use {func}`dask.array.to_zarr`, the data _cannot_ be read in using `anndata`'s functionality as `anndata` will look for its {doc}`specified file format metadata <anndata:fileformat-prose>`.

If you need to implement custom io, generally we found that using {func}`dask.array.map_blocks` provides a nice way.
See [our custom h5 io code] for an example.

## Advanced use and how-to-contribute

**How do `scanpy` and `anndata` handle sparse matrices?**

While there is some {class}`scipy.sparse.csr_matrix` and {class}`scipy.sparse.csc_matrix` support for `dask`, it is not comprehensive and missing key functions like summation, mean etc.
We have implemented custom functionality, much of which lives in {mod}`fast_array_utils`, although we have also had to implement custom algorithms like `pca` for sparse-in-dask.
In the future, an [`array-api`] compatible sparse matrix like [`finch`] would help us considerably as `dask` supports the [`array-api`].

Therefore, if you run into a puzzling error after trying to run a function like {func}`numpy.sum` (or similar) on a sparse-in-dask array, consider checking {mod}`fast_array_utils`.
If you need to implement the function yourself, see the next point.

**Custom block-wise array operations**

Sometimes you may want to do an operation on a an array that is implemented nowhere.
Generally, we have found {func}`dask.array.map_blocks` to be versatile enough that most operations can be expressed on it.
Take this (simplified) example of calculating a gram matrix from {func}`scanpy.pp.pca` for sparse-in-dask:

```python
def gram_block(x_part):
    gram_matrix = x_part.T @ x_part
    return gram_matrix[None, ...]

gram_matrix_dask = da.map_blocks(
    gram_block,
    x,
    new_axis=(1,),
    chunks=((1,) * x.blocks.size, (x.shape[1],), (x.shape[1],)),
    meta=np.array([], dtype=x.dtype),
    dtype=x.dtype,
).sum(axis=0)
```

This algorithm goes through every `chunk_size` number of rows and calculates the gram matrix for those rows producing a collection of `(n_vars,n_vars)` size matrix.
These are the summed together to produce a single `(n_vars,n_vars)` matrix, which is the gram amtrix.

Because `dask` does not implement matrix multiplication for sparse-in-dask, we do it ourselves.
We use `map_blocks` over a CSR sparse-in-dask array where the chunking looks something like `(chunk_size, n_vars)`.
When we compute the invdividual block's gram matrix, we add an axis via `[None, ...]` so that we can sum over that axis i.e., the `da.map_blocks` call produces a `(n_obs // chunk_size, n_vars, n_vars)` sized-matrix which is summed over the first dimension.
However, to make this work, we need to be very specific about how `da.map_blocks` expects its result to look like, done via `new_axis` and `chunks` `new_axis` indicates that we are adding a single new axis at the front.
The `chunks` argument specifices that the output of `da.map_blocks` should have `x.blocks.size` number of `(1, n_vars, n_vars)` matrixes.
This `chunks` argument thus allows the inferral of the shape of the output.

While this example is a bit complicated it shows how you can go from a matrix of one shape and chunking to another by operating in a clean way over blocks.

## FAQ

**What is `persist` for in RSC noteboooks?**

In the {doc}`multi-gpu showcase notebook for rapids-singlecell <rapids-singlecell:notebooks/06-multi_gpu_show>`, {meth}`dask.array.Array.persist` appears across the notebook.
This loads the entire dataset into memory while keeping the representation as a dask array.
Thus, lazy computation still works but only necessitates a single read into memory.
The catch is that you have enough memory to use `persist`.

**I'm out of memory, what now?**

You can alawys reduce the number of workers you use, which will cause more memory to be allocated per worker.
Some algorithms may have limitations with loading all data onto a single node; see {issue}`dask/dask-ml#985` for an example.

**How do I choose chunk sizes?**

Have a look at the {doc}`dask docs for chunking <dask:array-chunks>`, however the general rule of thumb there is to use larger chunks in memory than on disk.
In this sense, it is probably a good idea to use the largest chunk size in memory allowable by your memory limits (and the algorithms you use) in order to maximize any thread-level parallelization in algorithms to its fullest.
For sparse data, where the chunks in-memory do not map to those on disk, maxing out the memory available by choosing a large chunk size becomes more imperative.

[`dask` extension]: https://marketplace.visualstudio.com/items?itemName=joyceerhl.vscode-das
[our custom h5 io code]: https://github.com/scverse/anndata/blob/089ed929393a02200b389395f278b7c920e5bc4a/src/anndata/_io/specs/lazy_methods.py#L179-L20
[`array-api`]: https://data-apis.org/array-api/latest/index.html
[`finch`]: https://github.com/finch-tensor/finch-tensor-python
