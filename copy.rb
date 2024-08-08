require 'fileutils'
require 'pry'

# Method to read MP3 file paths from the given file
def read_mp3_paths(file_path)
  mp3_paths = []
  File.open(file_path, 'r') do |file|
    file.each_line do |line|
      line.chomp!
      match =  line.downcase.match(/"(.+\.mp3)"/)
      mp3_paths << match[1] if match
    end
  end
  mp3_paths
end

# Method to copy MP3 files to the specified directory
def copy_mp3_files(mp3_paths, destination_dir)
  FileUtils.mkdir_p(destination_dir) unless Dir.exist?(destination_dir)
  mp3_paths.each do |mp3_path|
    if File.exist?(mp3_path)
      FileUtils.cp(mp3_path, destination_dir)
      puts "Copied: #{mp3_path} to #{destination_dir}"
    else
      puts "File not found: #{mp3_path}"
    end
  end
end

# Main method to parse arguments and perform the copy operation
def main
  if ARGV.length != 2
    puts "Usage: ruby copy.rb <input_file> <destination_directory>"
    exit
  end

  input_file = ARGV[0]
  destination_dir = ARGV[1]

  unless File.exist?(input_file)
    puts "Input file not found: #{input_file}"
    exit
  end

  mp3_paths = read_mp3_paths(input_file)
  copy_mp3_files(mp3_paths, destination_dir)
end

if __FILE__ == $PROGRAM_NAME
  p 'TURE'
  main
else
  p 'HOLA'
  p $PROGRAM_NAME
end

