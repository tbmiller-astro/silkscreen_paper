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


rule plotPal13:
  output: 'src/tex/figures/ESO_294_10_post_corner.pdf', 'src/tex/figures/ESO_294_10_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=102,
    name="ESO_294_10",
    st=0.2,
    Q=0.4
  script: "src/scripts/plot_gc.py"