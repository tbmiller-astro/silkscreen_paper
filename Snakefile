rule plotPal4:
  output: 'src/tex/figures/Pal4_post_corner.pdf', 'src/tex/figures/Pal4_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=100,
    name="Pal4",
  script: "src/scripts/plot_gc.py"

rule plotPal13:
  output: 'src/tex/figures/Pal13_post_corner.pdf', 'src/tex/figures/Pal13_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=101,
    name="Pal13",
  script: "src/scripts/plot_gc.py"

rule plotE29410:
  output: 'src/tex/figures/ESO_294_10_post_corner.pdf', 'src/tex/figures/ESO_294_10_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=103,
    name="ESO_294_10",
    Q=0.4,
    st=0.2
  notebook: "src/scripts/plot_scul_dw.ipynb"

  rule plotE41005:
    output: 'src/tex/figures/ESO_410_05_post_corner.pdf', 'src/tex/figures/ESO_410_05_ims_post.pdf'
    conda: "silkscreen.yml"
    params:
      seed=104,
      name="ESO_410_05",
      Q=0.4,
      st=0.2
    notebook: "src/scripts/plot_scul_dw.ipynb"
