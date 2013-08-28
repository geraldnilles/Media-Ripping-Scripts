#! /usr/bin/env python

## Import Libs
import subprocess
import argparse

# Generic function for running a shell command
def cmd(cmd):
	subprocess.call(cmd)

# Rip All
#
# Rips an entire DVD from the disk to the raw/ folder
def rip_all():
	rip(["all"])


# Rip Title
# 
# Rips the provided list of titls to the raw folder
def rip(titles):
	for t in titles:
		cmd("makemkvcon mkv disc:1 "+t+" raw")

#-------------
# Transfer Funtions
#-------------

## Upload a local file to a Samba Share
def upload_to_SMB(filename,path):
	pass

## Download a local file from the Samba Share
def download_from_SMB(path):
	pass

#---------------
# Video Transcode Functions
#---------------

# Transcode Video
def transcode_video(filename):
	transcode_video_x264(filename)

def transcode_video_x264(filename):
	# Strip MPEG2 video to video.mpeg2
	# TODO This assumes video is the first track. Adjust to find the video
	# track
	cmd(["mkvextract", "tracks", filename, "1:video.mpeg2"])
	# Strip the timecodes
	cmd(["mkvextract", "timecodes_v2", filename, "1:timecodes.txt"])

	# Convert Video to H264
	cmd(["avconv", "-i", "video.mpeg2", "-c:v", "libx264", "-preset", "veryslow", "-crf", "20" ,"video.h264"])

	# Replace MPEG2 with H264
	cmd(["mkvmerge", "-o", filename+".h264.mkv", "--timecodes", "0:timecodes.txt", "video.h264", "-D", filename])

	cmd(["rm", "video.h264", "video.mpeg2", "timecodes.txt"])



#-------------------
# Audio Transcode Functions
#-------------------

# Transcode Audio
def transcode_audio(filename):
	pass

def transcode_audio_aac(filename):
	pass

def transcode_audio_opus(filename):
	
	cmd("ffmpeg -i audio.ac3 -c:a opus -b:a 384k -ac audio.opus")

# Strips all Audio except english
def only_english(filename):
	pass


# Generic Transcode Function
def transcode(filename):
	transcode_video(filename)
	transcode_audio(filename)


#----------------
# Post-Rip Clean-up functions
#----------------

## TV Cleanup
#
# Selects all of the videos that are a similar size.  This avoids the small 
# filler tracks as well as any "Play All" tracks
def tv_cleanup(mkvs):
	# Get the sizes of each MKVs
	mkv_sizes = []
	for m in mkvs:
		mkv_sizes.append(size(m))

	mkv_std_devs = []
	for m in mkv_sizes:
		# Calculate the Standard Deviation with m as the mean
		# Find the point that has the lowest standard deviation
	
	min_std_dev = min(mkv_std_devs)

	# From the lowest standard deviation point, delete all devices outside
	

## Movie Cleanup
#
# Selects the largest MKV file and deletes the rest
def movie_cleanup(mkvs):
	# TODO Use a lambda function instead of a for loop
	max_size = 0
	max_file = ""
	for m in mkvs:
		size = os.path.size(m)
		if size > max_size:
			max_size = size

	mkvs = [max_file]
	


def run(args):
	# Create a bank list of MKVs to rip
	mkvs = []
	if not args.only_convert:
		# Convert Disc to MKVs usign MakeMKV binary
		mkvs = rip(args.name[0])
		# Clean up MKVs
		if args.tv:
			# Only keep similarly sized video files
			tv_cleanup(mkvs)
		else:
			# Only keep the largest video file
			move_cleanup(mkvs)
		

	if len(mkvs) == 0:
		mkvs = args.name
	if not args.only_rip:
		for mkv in args.name:
			transcode(mkv,args.video,args.audio,args.only_english)

def parse_args():
	parser = argparse.ArgumentParser(description="Media Ripping Script")
	# Select Movie or TV mode
	parser.add_argument("-m","--movie",action="store_true") 
	parser.add_argument("-t","--tv",action="store_true")
	# Add argument for selecting video codec. x264 is default
	parser.add_argument(
			"-v","--video",
			choices=["copy","x264"],
			default="x264")
	# Add argument for selecting the audio codec.  Copying is default
	parser.add_argument(
			"-a","--audio",
			choices=["copy","aac","opus"],
			default="copy") 
	# Add option for only saving english tracks
	parser.add_argument("-e","--only-english",action="store_true")
	# Add option for ripping only
	parser.add_argument("-r","--only-rip",action="store_true")
	# Add option for transcoding only
	parser.add_argument("-c","--only-convert",action="store_true")
	# Add option for naming the video
	parser.add_argument("name")
	# Conver the arguments into a namespace
	args = parser.parse_args()
	# Run the script
	run(args)


if __name__ == "__main__":
	parse_args()

