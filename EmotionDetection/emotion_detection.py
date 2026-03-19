import requests
import json

def emotion_detector(text_to_analyze):
    """
    Function to detect emotions in text using Watson NLP Emotion Predict API
    
    Args:
        text_to_analyze (str): The text to analyze for emotions
        
    Returns:
        dict: Dictionary containing emotion scores and dominant emotion
    """
    
    # Define the URL for the emotion prediction API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Define the headers with the required model ID
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Create the input JSON object with the text to analyze
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        # Make the POST request to the API
        response = requests.post(url, headers=headers, json=input_json)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Convert the response text into a dictionary
        response_dict = json.loads(response.text)
        
        # Extract the emotions dictionary from the response
        # The exact path may vary based on the API response structure
        # Adjust this path according to the actual API response format
        emotions = response_dict.get('emotionPredictions', [{}])[0].get('emotion', {})
        
        # Extract the required emotions with their scores
        anger_score = emotions.get('anger', 0)
        disgust_score = emotions.get('disgust', 0)
        fear_score = emotions.get('fear', 0)
        joy_score = emotions.get('joy', 0)
        sadness_score = emotions.get('sadness', 0)
        
        # Create a dictionary of emotions and their scores for finding dominant emotion
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Find the dominant emotion (emotion with highest score)
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Create the formatted output
        formatted_output = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
        
        return formatted_output
        
    except requests.exceptions.RequestException as e:
        # Handle any request errors
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
            'error': f"Request failed: {str(e)}"
        }
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        # Handle any parsing errors
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
            'error': f"Error parsing response: {str(e)}"
        }
    except Exception as e:
        # Handle any other errors
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
            'error': f"Unexpected error: {str(e)}"
        }

# For testing the function
if __name__ == "__main__":
    # Test the function with different sample texts
    test_texts = [
        "I love this new technology!",
        "I am so happy today!",
        "This is frustrating and makes me angry",
        "I'm worried about the future",
        "This is sad news"
    ]
    
    for text in test_texts:
        print(f"\n{'='*50}")
        print(f"Testing with: '{text}'")
        print(f"{'='*50}")
        result = emotion_detector(text)
        
        # Print the result in a readable format
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Anger: {result['anger']}")
            print(f"Disgust: {result['disgust']}")
            print(f"Fear: {result['fear']}")
            print(f"Joy: {result['joy']}")
            print(f"Sadness: {result['sadness']}")
            print(f"Dominant emotion: {result['dominant_emotion']}")
