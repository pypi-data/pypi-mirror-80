


        if args.processes == None:
            args.processes = multiprocessing.cpu_count()
        threads = args.processes
        indices_list = get_contiguous_indices(threads, full_expression.shape[0])
        
        ray.init()

        ###########
        if not args.hdf5:
            ray_full_expression = ray.put(full_expression)
        else:
            ## make copies of the input hdf5 file
            hdf5_file_list = []
            for t in range(threads):
                hdf5_file_list.append(args.infile+"_"+str(t))
                cmd('cp '+args.infile+" "+hdf5_file_list[-1])
        ###########

        r_jobs = []
        for t in range(threads):
            if not args.hdf5:
                r_jobs.append(ray_get_global_cell_type_aov_stats.remote(indices_list[t], 
                                                                        ray_full_expression,
                                                                        list_of_k_sample_indices))
            else:
                r_jobs.append(ray_get_global_cell_type_aov_stats.remote(indices_list[t], 
                                                                        None,
                                                                        list_of_k_sample_indices,
                                                                        hdf5_file = hdf5_file_list[t]))
        temp_r_results = ray.get(r_jobs)
        ray.shutdown()
        ########################################
    
        global_percent_express_dict_list = []
        global_non_zero_mean_dict_list = []
        k_group_percent_express_dict_list = []
        non_zero_mean_expression_dict_list = []
        all_aov_results = []

        for t in range(len(temp_r_results)):
            global_percent_express_dict_list.append(temp_r_results[t][0])
            global_non_zero_mean_dict_list.append(temp_r_results[t][1])
            k_group_percent_express_dict_list.append(temp_r_results[t][2])
            non_zero_mean_expression_dict_list.append(temp_r_results[t][3])
            all_aov_results.append(temp_r_results[t][4])

        global_percent_express = ray_dicts_to_array(global_percent_express_dict_list)
        global_non_zero_mean = ray_dicts_to_array(global_non_zero_mean_dict_list)
        k_group_percent_express = ray_dicts_to_array(k_group_percent_express_dict_list)
        non_zero_mean_expression = ray_dicts_to_array(non_zero_mean_expression_dict_list)
        all_aov_results = ray_dicts_to_array(temp_aov_results).tolist()

        global_percent_express = global_percent_express[:,0]
        global_non_zero_mean = global_non_zero_mean[:,0]

        print(global_percent_express)
        print(global_non_zero_mean)
        print(k_group_percent_express)
        print(non_zero_mean_expression)
        print(all_aov_results)


def pyminer_get_stats_main():


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	## global arguments
	parser.add_argument(
	    '-infile','-in','-i','-input',
	    dest='infile',
	    type=str)
	parser.add_argument(
	    "-sample_groups",
	    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
	    dest = 'sample_groups',
	    type = str)
	parser.add_argument(
	    "-classes",
	    help='if there are classes to compare, put the annotation table in this argument',
	    dest = 'class_file',
	    type = str)
	parser.add_argument(
	    "-within_group",
	    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
	    dest = 'within_group',
	    type = int)
	parser.add_argument(
	    "-out_dir","-o","-out",
	    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
	    dest = 'out_dir',
	    type = str)
	parser.add_argument(
	    "-species","-s",
	    help = 'what species is this? Must be gProfiler compatible.',
	    dest = 'species',
	    type = str,
	    default = 'hsapiens')
	parser.add_argument(
	    '-no_gProfile',
	    help = 'should we do the automated gprofiler results?',
	    default = False,
	    action = 'store_true')
	parser.add_argument(
	    "-FDR","-fdr","-fdr_cutoff",
	    help='The desired Benjamini-Hochberg False Discovery Rate (FDR) for multiple comparisons correction (default = 0.05)',
	    dest = 'FDR_cutoff',
	    type = float,
	    default = 0.05)
	parser.add_argument(
	    "-Zscore","-Z_score_cutoff","-Z","-zscore","-z",
	    help='The desired False Discovery Rate (FDR) for multiple comparisons correction (default = 0.05)',
	    dest = 'Zscore',
	    type = float,
	    default = 2.0)
	parser.add_argument(
	    '-hdf5',
	    help = 'The input file is an HDF5 file',
	    default = False,
	    action = 'store_true')
	parser.add_argument(
	    "-ID_list","-ids",
	    help = 'If we are using an hdf5 file, give the row-wise IDs in this new line delimeted file',
	    type = str)
	parser.add_argument(
	    "-columns","-cols",
	    help = 'If we are using an hdf5 file, give the column-wise IDs in this new line delimeted file',
	    type = str)
	parser.add_argument(
	    '-rows',
	    help = 'if the samples are in rows, and variables are in columns',
	    default = False,
	    action = 'store_true')
	parser.add_argument(
	    "-log",'-log2','-log_transform',
	    help='do a log transformation prior to clustering',
	    action = 'store_true',
	    default = False)
	parser.add_argument(
	    '-lin_norm',
	    help = 'should we normalize the rows before doing the stats?',
	    default = False,
	    action = 'store_true')
	parser.add_argument(
	    '-processes', '-p',
	    help = 'The number of processes to use. Default will be the number of available threads.',
	    default = None,
	    type = int)
	args = parser.parse_args()


	pyminer_get_stats_main(,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,
		                   ,)