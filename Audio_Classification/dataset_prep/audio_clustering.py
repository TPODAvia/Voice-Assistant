from audio_analysis import *
import os
import wave

if __name__ == "__main__":

	directory = '/home/vboxuser/Voice-Assistant/Audio_Classification/dataset_prep/data'
	n = 4
	print(f"The number of clusters is: {n}. Running, please wait...")
	audio_list, map_coords_objects = analyse_folder(directory)
	clusters = cluster(audio_list, map_coords_objects,n)

	# compare_clusters_folders(["./music_speech/music_wav", "./music_speech/speech_wav"], clusters)
	#the list of folders has to be changed if we deal with other datasets

	arrays = clusters
	# arrays = [
	# 	['acomic.wav', 'acomic2.wav', 'allison.wav'],
	# 	['amal.wav', 'austria.wav', 'bagpipe.wav'],
	# 	# Add more arrays as needed
	# ]

	input_path = directory
	output_base_path = '/home/vboxuser/Voice-Assistant/Audio_Classification/dataset_prep'

	for i, array in enumerate(arrays):
		folder_name = f"folder{i + 1}"
		output_path = os.path.join(output_base_path, folder_name)
		os.makedirs(output_path, exist_ok=True)

		for wav_file in array:
			input_file = os.path.join(input_path, wav_file)
			output_file = os.path.join(output_path, wav_file)

			with wave.open(input_file, 'rb') as wav_in:
				with wave.open(output_file, 'wb') as wav_out:
					wav_out.setparams(wav_in.getparams())
					wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))
		
	print("Finish")
