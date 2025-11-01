"""
Fuzzy Logic Evaluation System for Checkers AI
Implements Mamdani fuzzy inference with membership functions and rule base
"""

class FuzzyEvaluator:
    """
    Fuzzy logic evaluator for checkers board positions
    Combines multiple heuristics using fuzzy rules
    """
    
    def __init__(self):
        """Initialize fuzzy evaluator with membership functions and rules"""
        self.setup_membership_functions()
        self.setup_rule_base()
    
    def setup_membership_functions(self):
        """
        Define membership functions for fuzzy sets
        Each function maps a crisp input to fuzzy membership [0, 1]
        """
        # Material advantage: -30 to +30 (piece count difference)
        self.material_low = lambda x: self._trimf(x, [-30, -30, 0])
        self.material_medium = lambda x: self._trimf(x, [-15, 0, 15])
        self.material_high = lambda x: self._trimf(x, [0, 30, 30])
        
        # Mobility: 0 to 50 (number of legal moves)
        self.mobility_low = lambda x: self._trimf(x, [0, 0, 15])
        self.mobility_medium = lambda x: self._trimf(x, [10, 25, 40])
        self.mobility_high = lambda x: self._trimf(x, [35, 50, 50])
        
        # Center control: 0 to 10 (pieces in center squares)
        self.center_low = lambda x: self._trimf(x, [0, 0, 3])
        self.center_medium = lambda x: self._trimf(x, [2, 5, 8])
        self.center_high = lambda x: self._trimf(x, [7, 10, 10])
        
        # Safety: 0 to 10 (protected pieces and stacks)
        self.safety_low = lambda x: self._trimf(x, [0, 0, 3])
        self.safety_medium = lambda x: self._trimf(x, [2, 5, 8])
        self.safety_high = lambda x: self._trimf(x, [7, 10, 10])
        
        # Advancement: 0 to 20 (pieces close to promotion)
        self.advancement_low = lambda x: self._trimf(x, [0, 0, 6])
        self.advancement_medium = lambda x: self._trimf(x, [5, 10, 15])
        self.advancement_high = lambda x: self._trimf(x, [14, 20, 20])
        
        # Output score: -100 to +100
        self.score_very_bad = lambda x: self._trimf(x, [-100, -100, -50])
        self.score_bad = lambda x: self._trimf(x, [-75, -40, -10])
        self.score_neutral = lambda x: self._trimf(x, [-20, 0, 20])
        self.score_good = lambda x: self._trimf(x, [10, 40, 75])
        self.score_very_good = lambda x: self._trimf(x, [50, 100, 100])
    
    def _trimf(self, x, params):
        """
        Triangular membership function
        
        Args:
            x: Input value
            params: [a, b, c] where b is peak and a, c are edges
        
        Returns:
            Membership degree [0, 1]
        """
        a, b, c = params
        
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            if b == a:
                return 1.0
            return (x - a) / (b - a)
        else:  # b < x < c
            if c == b:
                return 1.0
            return (c - x) / (c - b)
    
    def setup_rule_base(self):
        """
        Define fuzzy rules in the form:
        IF material IS X AND mobility IS Y ... THEN score IS Z
        """
        self.rules = [
            # Excellent position rules
            {
                'conditions': [
                    ('material', 'high'),
                    ('mobility', 'high'),
                ],
                'conclusion': 'very_good',
                'weight': 1.0
            },
            {
                'conditions': [
                    ('material', 'high'),
                    ('center', 'high'),
                    ('safety', 'high'),
                ],
                'conclusion': 'very_good',
                'weight': 0.9
            },
            
            # Good position rules
            {
                'conditions': [
                    ('material', 'high'),
                    ('mobility', 'medium'),
                ],
                'conclusion': 'good',
                'weight': 0.8
            },
            {
                'conditions': [
                    ('material', 'medium'),
                    ('mobility', 'high'),
                    ('center', 'high'),
                ],
                'conclusion': 'good',
                'weight': 0.8
            },
            {
                'conditions': [
                    ('advancement', 'high'),
                    ('safety', 'high'),
                ],
                'conclusion': 'good',
                'weight': 0.7
            },
            
            # Neutral position rules
            {
                'conditions': [
                    ('material', 'medium'),
                    ('mobility', 'medium'),
                ],
                'conclusion': 'neutral',
                'weight': 0.6
            },
            {
                'conditions': [
                    ('material', 'low'),
                    ('mobility', 'high'),
                    ('advancement', 'high'),
                ],
                'conclusion': 'neutral',
                'weight': 0.6
            },
            
            # Bad position rules
            {
                'conditions': [
                    ('material', 'low'),
                    ('mobility', 'low'),
                ],
                'conclusion': 'bad',
                'weight': 0.8
            },
            {
                'conditions': [
                    ('material', 'low'),
                    ('safety', 'low'),
                ],
                'conclusion': 'bad',
                'weight': 0.7
            },
            
            # Very bad position rules
            {
                'conditions': [
                    ('material', 'low'),
                    ('mobility', 'low'),
                    ('safety', 'low'),
                ],
                'conclusion': 'very_bad',
                'weight': 1.0
            },
            {
                'conditions': [
                    ('material', 'low'),
                    ('center', 'low'),
                    ('advancement', 'low'),
                ],
                'conclusion': 'very_bad',
                'weight': 0.9
            },
        ]
    
    def fuzzify(self, feature, value):
        """
        Fuzzify a crisp input value
        
        Args:
            feature: Feature name (material, mobility, center, safety, advancement)
            value: Crisp input value
        
        Returns:
            Dictionary of membership degrees for each fuzzy set
        """
        if feature == 'material':
            return {
                'low': self.material_low(value),
                'medium': self.material_medium(value),
                'high': self.material_high(value),
            }
        elif feature == 'mobility':
            return {
                'low': self.mobility_low(value),
                'medium': self.mobility_medium(value),
                'high': self.mobility_high(value),
            }
        elif feature == 'center':
            return {
                'low': self.center_low(value),
                'medium': self.center_medium(value),
                'high': self.center_high(value),
            }
        elif feature == 'safety':
            return {
                'low': self.safety_low(value),
                'medium': self.safety_medium(value),
                'high': self.safety_high(value),
            }
        elif feature == 'advancement':
            return {
                'low': self.advancement_low(value),
                'medium': self.advancement_medium(value),
                'high': self.advancement_high(value),
            }
        else:
            raise ValueError(f"Unknown feature: {feature}")
    
    def apply_rules(self, fuzzy_inputs):
        """
        Apply fuzzy rules to determine output membership
        
        Args:
            fuzzy_inputs: Dictionary of fuzzified inputs
                Example: {'material': {'low': 0.2, 'medium': 0.8, 'high': 0.0}, ...}
        
        Returns:
            Dictionary of output memberships for each conclusion
        """
        output_memberships = {
            'very_bad': 0.0,
            'bad': 0.0,
            'neutral': 0.0,
            'good': 0.0,
            'very_good': 0.0,
        }
        
        # Evaluate each rule
        for rule in self.rules:
            # Calculate rule activation (minimum of all conditions)
            activation = 1.0
            
            for feature, fuzzy_set in rule['conditions']:
                if feature in fuzzy_inputs:
                    membership = fuzzy_inputs[feature].get(fuzzy_set, 0.0)
                    activation = min(activation, membership)
            
            # Weight the activation
            activation *= rule['weight']
            
            # Update output membership (maximum aggregation)
            conclusion = rule['conclusion']
            output_memberships[conclusion] = max(
                output_memberships[conclusion],
                activation
            )
        
        return output_memberships
    
    def defuzzify(self, output_memberships):
        """
        Convert fuzzy output to crisp score using centroid method
        
        Args:
            output_memberships: Dictionary of output fuzzy memberships
        
        Returns:
            Crisp score value
        """
        # Define centroid for each output fuzzy set
        centroids = {
            'very_bad': -75,
            'bad': -35,
            'neutral': 0,
            'good': 35,
            'very_good': 75,
        }
        
        # Calculate weighted average (centroid defuzzification)
        numerator = 0.0
        denominator = 0.0
        
        for fuzzy_set, membership in output_memberships.items():
            if membership > 0:
                numerator += centroids[fuzzy_set] * membership
                denominator += membership
        
        if denominator == 0:
            return 0.0  # Neutral if no rules fired
        
        return numerator / denominator
    
    def evaluate(self, material, mobility, center, safety, advancement):
        """
        Evaluate board position using fuzzy logic
        
        Args:
            material: Material advantage (-30 to +30)
            mobility: Number of legal moves (0 to 50)
            center: Center control score (0 to 10)
            safety: Safety score (0 to 10)
            advancement: Advancement score (0 to 20)
        
        Returns:
            Crisp evaluation score
        """
        # Fuzzify all inputs
        fuzzy_inputs = {
            'material': self.fuzzify('material', material),
            'mobility': self.fuzzify('mobility', mobility),
            'center': self.fuzzify('center', center),
            'safety': self.fuzzify('safety', safety),
            'advancement': self.fuzzify('advancement', advancement),
        }
        
        # Apply fuzzy rules
        output_memberships = self.apply_rules(fuzzy_inputs)
        
        # Defuzzify to get crisp score
        score = self.defuzzify(output_memberships)
        
        return score


def extract_features_from_board(board, color):
    """
    Extract fuzzy evaluation features from board state
    
    Args:
        board: Board object
        color: Color to evaluate for
    
    Returns:
        Tuple of (material, mobility, center, safety, advancement)
    """
    from constants import PLAYER1_COLOR, PLAYER2_COLOR, ROWS, COLS
    
    # Material calculation
    if color == PLAYER1_COLOR:
        my_pieces = board.red_left
        my_kings = board.red_kings
        opp_pieces = board.white_left
        opp_kings = board.white_kings
    else:
        my_pieces = board.white_left
        my_kings = board.white_kings
        opp_pieces = board.red_left
        opp_kings = board.red_kings
    
    # Material = (my_pieces + 2*my_kings) - (opp_pieces + 2*opp_kings)
    material = (my_pieces + 2 * my_kings) - (opp_pieces + 2 * opp_kings)
    
    # Mobility = count of legal moves
    mobility = 0
    for piece in board.get_all_pieces(color):
        mobility += len(board.get_valid_moves(piece))
    
    # Center control = count pieces in center 4x4
    center_rows = range(ROWS // 2 - 1, ROWS // 2 + 2)
    center_cols = range(COLS // 2 - 1, COLS // 2 + 2)
    center = 0
    
    for row in center_rows:
        for col in center_cols:
            if 0 <= row < ROWS and 0 <= col < COLS:
                stack = board.get_stack(row, col)
                if stack and len(stack) > 0 and stack[0].color == color:
                    center += len(stack)  # Count all pieces in stack
    
    # Safety = count of protected pieces (adjacent friendly pieces)
    safety = 0
    my_piece_positions = set()
    for piece in board.get_all_pieces(color):
        my_piece_positions.add((piece.row, piece.col))
    
    for row, col in my_piece_positions:
        # Check diagonal neighbors
        neighbors = [
            (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)
        ]
        for nr, nc in neighbors:
            if (nr, nc) in my_piece_positions:
                safety += 1
                break  # Count piece once if it has any protection
        
        # Bonus for stacks (inherently safer)
        stack_size = board.get_stack_size(row, col)
        if stack_size >= 2:
            safety += 1
        if stack_size >= 3:
            safety += 1  # Triple stacks are very safe
    
    # Advancement = pieces close to promotion line
    advancement = 0
    for piece in board.get_all_pieces(color):
        if not piece.king:
            if color == PLAYER1_COLOR:
                # Red moves toward row 0
                distance_to_promotion = piece.row
                advancement += (ROWS - 1 - distance_to_promotion) * 0.5
            else:
                # White moves toward row 7
                distance_to_promotion = ROWS - 1 - piece.row
                advancement += (ROWS - 1 - distance_to_promotion) * 0.5
        
        # Stack advancement bonus
        stack_size = board.get_stack_size(piece.row, piece.col)
        if stack_size >= 2:
            advancement += 1
    
    return material, mobility, center, safety, advancement
