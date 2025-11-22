"""
Learning resources mapping for different topics and keywords
"""

LEARNING_RESOURCES = {
    # Computer Science & Programming
    'algorithm': {
        'title': 'Algorithms',
        'links': [
            {'name': 'GeeksforGeeks Algorithms', 'url': 'https://www.geeksforgeeks.org/fundamentals-of-algorithms/'},
            {'name': 'Wikipedia - Algorithm', 'url': 'https://en.wikipedia.org/wiki/Algorithm'},
            {'name': 'Khan Academy - Algorithms', 'url': 'https://www.khanacademy.org/computing/computer-science/algorithms'}
        ]
    },
    'data': {
        'title': 'Data Structures',
        'links': [
            {'name': 'GeeksforGeeks Data Structures', 'url': 'https://www.geeksforgeeks.org/data-structures/'},
            {'name': 'Wikipedia - Data Structure', 'url': 'https://en.wikipedia.org/wiki/Data_structure'},
            {'name': 'Programiz Data Structures', 'url': 'https://www.programiz.com/dsa'}
        ]
    },
    'network': {
        'title': 'Computer Networks',
        'links': [
            {'name': 'GeeksforGeeks Computer Networks', 'url': 'https://www.geeksforgeeks.org/computer-network-tutorials/'},
            {'name': 'Wikipedia - Computer Network', 'url': 'https://en.wikipedia.org/wiki/Computer_network'},
            {'name': 'Cisco Networking Basics', 'url': 'https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/networking-basics.html'}
        ]
    },
    'machine': {
        'title': 'Machine Learning',
        'links': [
            {'name': 'GeeksforGeeks Machine Learning', 'url': 'https://www.geeksforgeeks.org/machine-learning/'},
            {'name': 'Wikipedia - Machine Learning', 'url': 'https://en.wikipedia.org/wiki/Machine_learning'},
            {'name': 'Coursera ML Course', 'url': 'https://www.coursera.org/learn/machine-learning'}
        ]
    },
    'learning': {
        'title': 'Deep Learning',
        'links': [
            {'name': 'Deep Learning Tutorial', 'url': 'https://www.geeksforgeeks.org/deep-learning-tutorial/'},
            {'name': 'Wikipedia - Deep Learning', 'url': 'https://en.wikipedia.org/wiki/Deep_learning'},
            {'name': 'TensorFlow Tutorials', 'url': 'https://www.tensorflow.org/tutorials'}
        ]
    },
    'neural': {
        'title': 'Neural Networks',
        'links': [
            {'name': 'Neural Networks Explained', 'url': 'https://www.geeksforgeeks.org/neural-networks-a-beginners-guide/'},
            {'name': 'Wikipedia - Neural Network', 'url': 'https://en.wikipedia.org/wiki/Neural_network'},
            {'name': 'MIT Neural Networks Course', 'url': 'https://ocw.mit.edu/courses/brain-and-cognitive-sciences/'}
        ]
    },
    'language': {
        'title': 'Natural Language Processing',
        'links': [
            {'name': 'NLP Tutorial', 'url': 'https://www.geeksforgeeks.org/natural-language-processing-nlp-tutorial/'},
            {'name': 'Wikipedia - NLP', 'url': 'https://en.wikipedia.org/wiki/Natural_language_processing'},
            {'name': 'NLTK Documentation', 'url': 'https://www.nltk.org/'}
        ]
    },
    'database': {
        'title': 'Database Systems',
        'links': [
            {'name': 'Database Tutorial', 'url': 'https://www.geeksforgeeks.org/dbms/'},
            {'name': 'Wikipedia - Database', 'url': 'https://en.wikipedia.org/wiki/Database'},
            {'name': 'W3Schools SQL', 'url': 'https://www.w3schools.com/sql/'}
        ]
    },
    'programming': {
        'title': 'Programming Concepts',
        'links': [
            {'name': 'Programming Fundamentals', 'url': 'https://www.geeksforgeeks.org/fundamentals-of-programming/'},
            {'name': 'Wikipedia - Programming', 'url': 'https://en.wikipedia.org/wiki/Computer_programming'},
            {'name': 'Codecademy', 'url': 'https://www.codecademy.com/'}
        ]
    },
    'software': {
        'title': 'Software Engineering',
        'links': [
            {'name': 'Software Engineering Tutorial', 'url': 'https://www.geeksforgeeks.org/software-engineering/'},
            {'name': 'Wikipedia - Software Engineering', 'url': 'https://en.wikipedia.org/wiki/Software_engineering'},
            {'name': 'IEEE Software Engineering', 'url': 'https://www.computer.org/csdl/magazine/so'}
        ]
    }
}

def get_learning_resources(keyword):
    """
    Get learning resources for a given keyword
    Returns a list of relevant learning links
    """
    keyword_lower = keyword.lower()
    
    # Direct match
    if keyword_lower in LEARNING_RESOURCES:
        return LEARNING_RESOURCES[keyword_lower]
    
    # Partial match
    for key, resources in LEARNING_RESOURCES.items():
        if key in keyword_lower or keyword_lower in key:
            return resources
    
    # Default resources for general topics
    return {
        'title': f'Learn about {keyword}',
        'links': [
            {'name': f'Wikipedia - {keyword}', 'url': f'https://en.wikipedia.org/wiki/{keyword.replace(" ", "_")}'},
            {'name': f'Google Search - {keyword}', 'url': f'https://www.google.com/search?q={keyword.replace(" ", "+")}+tutorial'},
            {'name': f'YouTube - {keyword}', 'url': f'https://www.youtube.com/results?search_query={keyword.replace(" ", "+")}+tutorial'}
        ]
    }
