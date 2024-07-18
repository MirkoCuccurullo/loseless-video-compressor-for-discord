import ffmpeg as ffmpeg
import os
import sys

def get_video_duration(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f'Error occurred while probing video: {e.stderr.decode()}', file=sys.stderr)
        return None

def compress_video_to_target_size(input_file, output_file, target_size_mb, audio_bitrate='128k'):
    try:
        # Get the duration of the input video
        duration = get_video_duration(input_file)
        if duration is None:
            return

        # Convert target size to bits
        target_size_bits = target_size_mb * 8 * 1024 * 1024
        
        # Estimate the target bitrate in bits per second
        target_bitrate = (target_size_bits - (audio_bitrate_to_bits(audio_bitrate) * duration)) / duration
        
        # Ensure the initial bitrate is not too low
        min_bitrate = 100000  # 100 kbps minimum video bitrate to avoid extremely poor quality
        if target_bitrate < min_bitrate:
            print("The target bitrate is too low, increasing to minimum bitrate of 100 kbps.")
            target_bitrate = min_bitrate

        while True:
            print(f'Trying with video bitrate: {target_bitrate} bits/s')
            ffmpeg.input(input_file).output(output_file, video_bitrate=target_bitrate, audio_bitrate=audio_bitrate).run(overwrite_output=True)
            
            output_file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            if output_file_size_mb <= target_size_mb:
                print(f'Video compressed successfully and saved as {output_file}')
                print(f'The output file size is {output_file_size_mb:.2f} MB, which is within the target size of {target_size_mb} MB.')
                break
            else:
                print(f'The output file size is {output_file_size_mb:.2f} MB, which is larger than the target size of {target_size_mb} MB.')
                target_bitrate = target_bitrate * 0.9  # Reduce bitrate by 10% and try again

    except ffmpeg.Error as e:
        print(f'Error occurred during compression: {e.stderr.decode()}', file=sys.stderr)

def audio_bitrate_to_bits(audio_bitrate):
    if audio_bitrate.endswith('k'):
        return int(audio_bitrate[:-1]) * 1000
    elif audio_bitrate.endswith('M'):
        return int(audio_bitrate[:-1]) * 1000000
    else:
        return int(audio_bitrate)

if __name__ == "__main__":
    input_file = 'input.mp4'  # Replace with your input file path
    output_file = 'output.mp4'  # Replace with your output file path
    target_size_mb = 25  # Target size in megabytes

    compress_video_to_target_size(input_file, output_file, target_size_mb)
