num_procs=4
num_tasks=16

python train_greedy_np.py \
--num_procs=$num_procs       \
--num_tasks=$num_tasks      \
--range_l=0.10      \
--range_r=1.90 

python train_greedy_np.py \
--num_procs=$num_procs       \
--num_tasks=$num_tasks      \
--range_l=2.00      \
--range_r=3.90 

