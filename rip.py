#! /usr/bin/env python

## Import Libs
import subprocess
import argparse

# Generic function for running a shell command
def cmd(cmd):
	subprocess.call(cmd)

## Rip Title
# 
# Rips the provided list of titls to the raw folder
#
# @param disc_name - The name of the disk you are ripping
# @return a list of MKV files created
def rip(disc_name):
	rip_folder = "rip/"+disc_name
	os.mkdir(rip_folder)
	cmd("makemkvcon mkv dev:dvd all "+rip_folder)
	return rip_folder

#-------------
# Transfer Funtions
#-------------

## Upload a local file to the HTTP server
#
# Upload a local file to the media server using HTTP.
#
# @param local_path - Local path to the file you want to upload
# @param media_type - Type of Media.  Options right now are "tv" and "movie"
# @return returns 0 is successful.
def upload_media_server(local_path,media_type):
	# HTTP Upload
	pass


#---------------
# Video Transcode Functions
#---------------

# Transcode Video
def transcode_video(infile,outfile):
	transcode_video_x264(infile,outfile)

def transcode_video_x264(infile, outfile):
	# Strip MPEG2 video to video.mpeg2
	# TODO This assumes video is the first track. Adjust to find the video
	# track
	cmd(["mkvextract", "tracks", infile, "1:video.mpeg2"])

	# Strip the timecode file
	cmd(["mkvextract", "timecodes_v2", infile, "1:timecodes.txt"])

	# Convert Video to H264
	cmd(["avconv", "-i", "video.mpeg2", "-c:v", "libx264", "-preset", "veryslow", "-crf", "20" ,"video.h264"])

	# Replace MPEG2 with H264
	cmd(["mkvmerge", "-o", outfile, "--timecodes", "0:timecodes.txt", "video.h264", "-D", infile])

	# Remove the temporary files
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
def tv_cleanup(rip_folder):
	# Generate a list of mkvs from rip folder
	mkvs = []
	for x in os.listdir(rip_folder):
		mkvs.append({
			"path":rip_folder+"/"+x,
			"size":	os.path.size(rip_folder+"/"+x),
			"stddev":0
			})
	
	# Calculate the standard deviation from each point
	for i in mkvs:
		for j in mkvs:
			i["stddev"] += (i["size"]-j["size"])**2

		i["stddev"] = i["stddev"]/len(mkvs)
		i["stddev"] = math.sqrt(i["stddev"])


	# Find the device with the smallest Stddev
	min_std_dev = min(mkv_std_devs)

		

## Movie Cleanup
#
# Selects the largest MKV file and deletes the rest
def movie_cleanup(rip_folder):
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
		rip_folder = rip(args.name[0])
		# Clean up MKVs
		if args.tv:
			# Only keep similarly sized video files
			mkvs = tv_cleanup(rip_folder)
		else:
			# Only keep the largest video file
			mkvs = move_cleanup(rip_folder)
	
	# If only converting, use the name object as the mkv list
	else:
		mkvs = args.name
	
	if not args.only_rip:
		for mkv in args.name:
			transcode(mkv,args.video,args.audio,args.only_english)

def parse_args():
	parser = argparse.ArgumentParser(description="Media Ripping Script")
	# Select TV mode - Multiple titles are ripped from the disk
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

