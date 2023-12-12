import torch
device = 'cpu'
import matplotlib.pyplot as plt
import corner
import os
import silkscreen
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.visualization import make_lupton_rgb
import paths
torch.manual_seed(snakemake.params['seed'])

name = snakemake.params['name']
gal_dir = f'{paths.data}/GCs/{name}/'

post_list = []
rounds = [0,1,2]
fig = plt.figure(figsize=(9,9))
## Plot posterior
param_names = [r'$\log M_* / M_\odot$', 'D (kpc)','[Fe/H]','Age (Gyr)']
for r in rounds:
    post = torch.load(f'{gal_dir}fall_2023_V4_posterior_round_{r}.pt', map_location=device, )
    post_list.append(post.sample(sample_shape=(20_000,),x = post.default_x).numpy())
    post_list[-1][:,1]*= 1e3
for r in rounds:
    if r == 0:
        fig = corner.corner(post_list[r], plot_density = False, plot_datapoints = False, color = f'C{r}',fig = fig, labels=param_names)
    elif r == rounds[-1]:
        corner.corner(post_list[r], plot_density = False, plot_datapoints = False, color = f'C{r}', fig = fig, show_titles= True,  labels=param_names, label_kwargs={'fontsize':17}, title_kwargs={'fontsize': 10})
    else:
        corner.corner(post_list[r], plot_density = False, plot_datapoints = False, color = f'C{r}', fig = fig,)
ax_text = fig.axes[1]
text_fs = 15
ax_text.text(0.0,.7,'Round 1', color = 'C0', ha = 'left', va = 'top',fontsize = text_fs, transform= ax_text.transAxes)
ax_text.text(0.0,.56,'Round 2', color = 'C1', ha = 'left', va = 'top',fontsize = text_fs, transform= ax_text.transAxes)
ax_text.text(0.0,.42,'Round 3', color = 'C2', ha = 'left', va = 'top',fontsize = text_fs, transform= ax_text.transAxes)
ax_text.text(0.,.99,name, color = 'k', ha = 'left', va = 'top',fontsize = text_fs+8, transform= ax_text.transAxes)

fig.savefig(f'{paths.figures}/{name}_post_corner.pdf')

#Simulate images from posterior
ra,dec = np.loadtxt(gal_dir + 'ra_dec.txt')
try:
    red_vec = silkscreen.utils.get_reddening(SkyCoord(ra,dec, unit = 'deg'), ['DECam_g','DECam_r', 'DECam_z'])
except FileNotFoundError:
    import dustmaps.sfd
    dustmaps.sfd.fetch()
    red_vec = silkscreen.utils.get_reddening(SkyCoord(ra,dec, unit = 'deg'), ['DECam_g','DECam_r', 'DECam_z'])

psfs = np.load(gal_dir+'psfs.npy')
psfs = psfs[:,31-15:31+15,31-15:31+15]

dist_dict = torch.load(gal_dir + 'dist_param_dict.pt')

obs_arr = torch.load(gal_dir+'cutout.pt').numpy()

iso_kwargs = dict(mag_limit=27, mag_limit_band='DECam_r')


obs = silkscreen.SilkScreenObservation(data = obs_arr, imager = 'DECam', filters = ['DECam_g','DECam_r', 'DECam_z'], sky_sb = [ 22.04, 20.91, 18.46],
exp_time = [87*2,67*2,100*2], pixel_scale = 0.262, zpt = 22.5, psf = psfs, distribution= 'plummer', distribution_kwargs=dist_dict, iso_kwargs=iso_kwargs,
extinction_reddening = red_vec)

simmer = silkscreen.simmer.SSPSimmer(obs)

inj_img = np.load(f'{gal_dir}/for_inj.npy')
post_im_samps = []
for theta_post in post_list[-1][:3]:
    x,y = np.random.randint(1000,2000, size = 2)
    inj_cutout = inj_img[:,x:x+obs_arr.shape[1], y:y+obs_arr.shape[2]]
    theta_use = torch.Tensor([theta_post[0],theta_post[1]/1.e3,theta_post[2],theta_post[3]])
    gal_img = simmer.get_image_for_injec(x = theta_use)
    fake_obs = gal_img+inj_cutout
    post_im_samps.append(fake_obs)

im_fig = plt.figure(figsize=(8,8))
st = 0.2
Q = 8
rgb_obs = make_lupton_rgb(obs_arr[2],obs_arr[1], obs_arr[0], stretch=st, Q = Q, minimum=-5e-2)

axes = im_fig.subplots(2,2)

for j,ax in enumerate(axes.flatten() ):
    ax.axis('off')
    if j == 0:
        ax.imshow(rgb_obs)
        #ax.set_title('Observed', fontsize = 18)
    else:
        im_cur = post_im_samps[j-1]
        rgb_cur = make_lupton_rgb(im_cur[2],im_cur[1], im_cur[0], stretch=st, Q = Q, minimum=-5e-2)
        ax.imshow(rgb_cur)
x_outline = [1,obs_arr.shape[1]-1, obs_arr.shape[1]-1, 1,1]
y_outline = [1,1,obs_arr.shape[1]-1, obs_arr.shape[1]-1,1]
axes[0][0].plot(x_outline,y_outline, '--', color = 'palegoldenrod', lw = 5,)
axes[0][0].text(0.02,0.97,'Observed', color = 'white', ha = 'left', va = 'top',fontsize = 20, transform= axes[0][0].transAxes)

im_fig.tight_layout()
im_fig.savefig(f'{paths.figures}/{name}_ims_post.pdf')