import scvi
import time
import numpy as np


adata = scvi.data.synthetic_iid(run_setup_anndata=False)

adata.layers["counts"] = adata.X.copy()

scvi.data.setup_anndata(
    adata,
    batch_key="batch",
    protein_expression_obsm_key="protein_expression"
)

vae1 = scvi.model.TOTALVI(adata, use_cuda=True, latent_distribution="normal")

scdl1 = vae1._make_scvi_dl(adata=adata, batch_size=16)

def time_scdl(scdl):
    for t in scdl:
        continue


start = time.time()
time_scdl(scdl1)
end = time.time()
print(end-start)

%timeit scdl1.dataset.data["X"]


adata2 = adata.copy()
scvi.data.setup_anndata(
    adata2,
    layer="counts",
    batch_key="batch",
    protein_expression_obsm_key="protein_expression"
)

vae2 = scvi.model.TOTALVI(adata2, use_cuda=True, latent_distribution="normal")

scdl2 = vae2._make_scvi_dl(adata=adata2, batch_size=16)


start = time.time()
time_scdl(scdl2)
end = time.time()
print(end-start)
