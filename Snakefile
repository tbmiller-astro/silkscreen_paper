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

rule plotE54032:
  output: 'src/tex/figures/ESO_540_32_post_corner.pdf', 'src/tex/figures/ESO_540_32_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=107,
    name="ESO_540_32",
    Q=0.1,
    st=0.1
  notebook: "src/scripts/plot_scul_dw.ipynb"

rule plotE34931:
  output: 'src/tex/figures/ESO_349_31_post_corner.pdf', 'src/tex/figures/ESO_349_31_ims_post.pdf'
  conda: "silkscreen.yml"
  params:
    seed=108,
    name="ESO_349_31",
    Q=0.2,
    st=0.2
  notebook: "src/scripts/plot_scul_dw.ipynb"

rule plot_self_test:
  output: 'src/tex/figures/self_test_post_corner.pdf', 'src/tex/figures/self_test_ims.pdf','src/tex/figures/self_test_sbc.pdf'
  conda: "silkscreen.yml"
  params:
    seed=105,
    name="self_test",
    Q=6.,
    st=0.15,
  notebook: "src/scripts/plot_self_test.ipynb"
