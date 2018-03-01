#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np,gzip,pickle,matplotlib.cm as cm,matplotlib.pyplot as plt,time

def extraction_base_mnist() :
	with gzip.open('./assets/mnist.pkl.gz', 'rb') as f:
		train_set, valid_set, test_set = pickle.load(f,encoding="latin1")
	train_x, train_y = train_set
	valid_x, valid_y = valid_set
	test_x, test_y = test_set

	if learning_type=="supervised" :
		train=[[],[],[],[],[],[],[],[],[],[]]
		image_number_at_label_changing=[0]
		toto=0
		for k in np.arange(len(train_x)) :
			train[train_y[k]].append(train_x[k])
		train_x=[]
		for k in np.arange(len(train)) :
			train_x+=train[k]
			toto+=len(train[k])
			image_number_at_label_changing.append(toto)
	y=image_number_at_label_changing
	homeo_instant=[]
	for m in np.arange(10) :
		for n in np.arange(5) :
			homeo_instant.append(y[m]+(y[m+1]-y[m])*(n+1)/5)

	return train_x,image_number_at_label_changing,homeo_instant

def sensor_spike_generator(p,train_x_local) :
	image_time=[]
	times=[]
	pixel_value=train_x_local[p]
	for u in np.arange(number_of_pixel):
		if train_x_local[p][u]>pxl_gray_lvl_threshold :
			for k in np.arange(int(runtime/(1.2e-6/pixel_value[u]))):
				tutu=abs(np.random.normal(loc=k*1.2e-6/pixel_value[u],scale=sigma))
				times.append([tutu+p*(runtime+img_delay),u])
	image_time.append(p*(runtime+img_delay))
	times.sort()
	return times

def neuron_initialization(n) :
	v=np.zeros(n)
	last_spike=np.ones(n)*t_ltd*1.05
	number_of_spike=np.zeros(n)
	inib_lateral=np.zeros(n)
	refract=np.zeros(n)
	threshold=1.0*np.ones(n)
	if learning_type=="supervised" :
		threshold[n//10:n]=threshold_max
	neuron=[v,last_spike,number_of_spike,threshold,inib_lateral,refract]
	return neuron

def synapse_initialization(nin,nout) :
	g_brut=gmin + (gmax-gmin)*np.random.rand(nin*nout)
	g=np.reshape(g_brut, (nin, nout))
	return g

def homeosthasie(p,inalc,neuron,number_of_spike_old) :
	number_of_spike_homeo_period=np.zeros(len(neuron[2]))
	for j in np.arange(len(neuron[2])) :
		number_of_spike_homeo_period[j]=neuron[2][j] - number_of_spike_old[j]
		number_of_spike_old[j]=neuron[2][j]
		neuron[3][j]+=homeostasis_on*neuron[3][j]*(number_of_spike_homeo_period[j]-170)/600
		neuron[3][j]=np.clip(neuron[3][j],threshold_min,threshold_max)
	n=len(neuron[0])
	if learning_type=="supervised" :
		for i in np.arange(len(inalc)-1) :
			if p==inalc[i] :
				neuron[3][0:(n/10)*i]=threshold_max
				neuron[3][(n/10)*i:(n/10)*(i+1)]=1.0
				neuron[3][(n/10)*(i+1):n]=threshold_max
			elif p>=inalc[i] and p<inalc[i+1] :
				neuron[3][0:(n/10)*i]=threshold_max
				neuron[3][(n/10)*(i+1):n]=threshold_max
	return [neuron,number_of_spike_old]

def range_random(integer_number) :
	items=np.arange(integer_number)
	np.random.shuffle(items)
	return items

def calcul_index_neuron_fire(threshold_out,v_out,g) :
	c=(threshold_out- v_out)*c_membrane/g + apulse_pre*tpulse
	i_out=np.argmin(c)
	min_c=np.min(c)
	t_out=tpulse+(-b-np.sqrt(b*b-4*a*min_c))/(2*a)
	aer_out=[t_out,i_out]
	return aer_out

def network (aer_in,t_last_event_in,neuron_in,g,neuron_out,feedback) :
	t_in=aer_in[0]
	i_in=aer_in[1]
	[v_in,last_spike_in,number_of_spike_in,threshold_in,inhib_lateral_in,refract_in]=neuron_in
	[v_out,last_spike_out,number_of_spike_out,threshold_out,inhib_lateral_out,refract_out]=neuron_out
	n_in=len(v_in)
	n_out=len(v_out)
	aer_out=[]
	w = g[i_in,:] *1.0/350000
	v_out = v_out * np.exp((-t_in + t_last_event_in)/to_leaky)
	v_out += w *  np.greater(t_in , inhib_lateral_out) * np.greater(t_in , refract_out)
	iout=np.where(np.greater(v_out , threshold_out)==1)[0]
	if len(iout) > 0 :
		np.random.shuffle(iout)
		i_out=iout[0]
		t_out = t_in
		v_out=np.zeros(n_out)
		number_of_spike_out[i_out]+=1
		aer_out=[t_out,i_out]
		refract_out[i_out]=t_out +  t_refractory
		inhib_lateral_out=(t_out+t_inhibitory)*np.ones(n_out)
		inhib_lateral_out[i_out]=t_out
		delta_t_in=t_out - last_spike_in
		dgpos=(gmax-g[:,i_out])*(a_plus*delta_t_in/alpha)*np.exp(-delta_t_in/to_plus)
		delta_t_in_neg=-t_feedback
		dgneg=g[:,i_out]*(a_moins*delta_t_in_neg/alpha)*np.exp(delta_t_in_neg/to_moins)
		testg=np.logical_and( np.greater(delta_t_in , 0.0) , np.less (delta_t_in , t_ltp ) )
		g[:,i_out] += np.where( testg , dgpos , dgneg )
		g[:,i_out] = np.clip( g[:,i_out] , gmin , gmax)
	last_spike_in[i_in]=t_in
	t_last_event_in=t_in
	neuron_in=[v_in,last_spike_in,number_of_spike_in,threshold_in,inhib_lateral_in,refract_in]
	neuron_out=[v_out,last_spike_out,number_of_spike_out,threshold_out,inhib_lateral_out,refract_out]
	return [aer_out,t_last_event_in,neuron_in,g,neuron_out]

def learning(gvars):
	globals().update(gvars)
	neuron1=neuron_initialization(n1)
	neuron2=neuron_initialization(n2)
	neuron3=neuron_initialization(n3)
	g12=synapse_initialization(n1,n2)
	g23=synapse_initialization(n2,n3)
	number_of_spike_old1=np.zeros(n1)
	number_of_spike_old2=np.zeros(n2)
	number_of_spike_old3=np.zeros(n3)
	t_last_event1=0
	train_x,image_number_at_label_changing,homeo_instant=extraction_base_mnist()
	print("homeo_instant=",homeo_instant)
	print("image_number_at_label_changing",image_number_at_label_changing)
	for p in np.arange(number_of_img) :
		if ((p+1) % homeo_period == 0) and (learning_type=="unsupervised") or (learning_type=="supervised") and (homeo_instant.count(p)!=0) :
			print(" ######################################################################")
			print("image_number=",p+1)
			[neuron2,number_of_spike_old2]=homeosthasie(p,image_number_at_label_changing,neuron2,number_of_spike_old2)
			[neuron3,number_of_spike_old3]=homeosthasie(p,image_number_at_label_changing,neuron3,number_of_spike_old3)
			print("threshold2=",neuron2[3])
			print("threshold3=",neuron3[3])
			print(" ######################################################################")
		aer_one_image=sensor_spike_generator(p,train_x)
		for n in np.arange(len(aer_one_image)) :
			aer1_one_ligne=aer_one_image[n]
			[aer2,t_last_event1,neuron1,g12,neuron2]=network(aer1_one_ligne,t_last_event1,neuron1,g12,neuron2,"feedback_on")
	return g12,g23

def affichage (g,n11_in,n12_in,n21_out,n22_out,figure_number,title,timestamp):
	n_out=n21_out*n22_out
	n_in=n11_in*n12_in
	for neuron_index in np.arange(n_out) :
		fig=plt.figure(figure_number)
		plt.subplot(n21_out,n22_out,neuron_index+1)
		titi=g[:,neuron_index]
		plt.axis('off')
		plt.imshow(titi.reshape((n11_in,n12_in))/gmax, vmin = 0, vmax = 1,cmap = plt.get_cmap('gray'), interpolation='none')
		plt.suptitle(title,fontsize=16)
	img_name="./assets/simulations/simulation_"+str(timestamp)+"/neuron_"+str(figure_number)+"_"+str(neuron_index)+"_"+str(timestamp)+".png"
	fig.savefig(img_name)
	return img_name
