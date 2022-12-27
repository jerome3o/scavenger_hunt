#! /bin/bash


# Get a list of all dirs in the clues/ dir
# and get the first letter of each dir if the letter is a number, and get the max
max_number=$(ls clues/ | grep -E '^[0-9]' | cut -c1 | sort -n | tail -n1)

# Function that makes a placeholder directory with text file
function make_placeholder {
  # Make a folder called X_placeholder where X is the first cli argument
  mkdir clues/$1_placeholder

  # Make a file called text.txt in that folder with the text "Placeholder clue X"
  echo "Placeholder clue $1" > clues/$1_placeholder/text.txt
}

# call make_placeholder for $max_number + 1 to $max_number + 10
for i in $(seq $((max_number + 1)) $((max_number + 10))); do
  make_placeholder $i
done
