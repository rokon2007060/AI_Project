"""
Performance Logging and Monitoring System for AI Agents
Tracks and analyzes AI performance metrics
"""
import time
import json
from datetime import datetime
from collections import defaultdict


class PerformanceLogger:
    """
    Logger for tracking AI performance metrics
    """
    
    def __init__(self, log_file='ai_performance.json'):
        """
        Initialize performance logger
        
        Args:
            log_file: Path to JSON log file
        """
        self.log_file = log_file
        self.current_game_data = None
        self.all_games = []
        self.move_history = []
    
    def start_game(self, agent1_name, agent2_name, game_id=None):
        """
        Start tracking a new game
        
        Args:
            agent1_name: Name of agent playing as PLAYER1 (Red)
            agent2_name: Name of agent playing as PLAYER2 (White)
            game_id: Optional game identifier
        """
        self.current_game_data = {
            'game_id': game_id or f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'agent1': agent1_name,
            'agent2': agent2_name,
            'moves': [],
            'winner': None,
            'total_moves': 0,
            'game_duration': 0,
        }
        self.move_history = []
    
    def log_move(self, agent_name, color, move_number, move_info, 
                 nodes_expanded=0, eval_time=0, was_capture=False,
                 board_state=None, stack_info=None):
        """
        Log a single move
        
        Args:
            agent_name: Name of agent making the move
            color: Color of the player
            move_number: Move number in game
            move_info: Tuple of (from_pos, to_pos)
            nodes_expanded: Number of nodes expanded in search
            eval_time: Time taken for evaluation
            was_capture: Whether move was a capture
            board_state: Optional board state snapshot
            stack_info: Optional info about stacks on board
        """
        if self.current_game_data is None:
            return
        
        move_data = {
            'move_number': move_number,
            'agent': agent_name,
            'color': 'red' if color == (255, 0, 0) else 'white',
            'from': move_info[0] if move_info else None,
            'to': move_info[1] if move_info else None,
            'nodes_expanded': nodes_expanded,
            'eval_time': eval_time,
            'was_capture': was_capture,
            'timestamp': datetime.now().isoformat(),
        }
        
        if stack_info:
            move_data['stack_info'] = stack_info
        
        self.current_game_data['moves'].append(move_data)
        self.move_history.append(move_data)
    
    def end_game(self, winner_name=None, reason='normal'):
        """
        End game tracking and save results
        
        Args:
            winner_name: Name of winning agent (or None for draw)
            reason: Reason for game end ('normal', 'stalemate', 'draw', 'timeout')
        """
        if self.current_game_data is None:
            return
        
        self.current_game_data['end_time'] = datetime.now().isoformat()
        self.current_game_data['winner'] = winner_name or 'draw'
        self.current_game_data['end_reason'] = reason
        self.current_game_data['total_moves'] = len(self.current_game_data['moves'])
        
        # Calculate game duration
        start_time = datetime.fromisoformat(self.current_game_data['start_time'])
        end_time = datetime.fromisoformat(self.current_game_data['end_time'])
        self.current_game_data['game_duration'] = (end_time - start_time).total_seconds()
        
        # Calculate per-agent statistics
        agent_stats = self._calculate_agent_stats()
        self.current_game_data['agent_stats'] = agent_stats
        
        # Save game data
        self.all_games.append(self.current_game_data)
        self._save_to_file()
        
        self.current_game_data = None
    
    def _calculate_agent_stats(self):
        """Calculate statistics for each agent in current game"""
        stats = defaultdict(lambda: {
            'moves': 0,
            'total_nodes': 0,
            'total_time': 0,
            'captures': 0,
            'avg_nodes_per_move': 0,
            'avg_time_per_move': 0,
        })
        
        for move in self.current_game_data['moves']:
            agent = move['agent']
            stats[agent]['moves'] += 1
            stats[agent]['total_nodes'] += move['nodes_expanded']
            stats[agent]['total_time'] += move['eval_time']
            if move['was_capture']:
                stats[agent]['captures'] += 1
        
        # Calculate averages
        for agent in stats:
            moves = stats[agent]['moves']
            if moves > 0:
                stats[agent]['avg_nodes_per_move'] = stats[agent]['total_nodes'] / moves
                stats[agent]['avg_time_per_move'] = stats[agent]['total_time'] / moves
        
        return dict(stats)
    
    def _save_to_file(self):
        """Save all game data to JSON file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.all_games, f, indent=2)
        except Exception as e:
            print(f"Error saving performance log: {e}")
    
    def get_agent_summary(self, agent_name):
        """
        Get summary statistics for a specific agent across all games
        
        Args:
            agent_name: Name of the agent
        
        Returns:
            Dictionary of statistics
        """
        summary = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_moves': 0,
            'total_nodes': 0,
            'total_time': 0,
            'total_captures': 0,
            'avg_nodes_per_game': 0,
            'avg_time_per_game': 0,
            'win_rate': 0,
        }
        
        for game in self.all_games:
            # Check if agent participated
            if agent_name not in [game['agent1'], game['agent2']]:
                continue
            
            summary['games_played'] += 1
            
            # Check win/loss
            if game['winner'] == agent_name:
                summary['wins'] += 1
            elif game['winner'] == 'draw':
                summary['draws'] += 1
            else:
                summary['losses'] += 1
            
            # Add stats if available
            if 'agent_stats' in game and agent_name in game['agent_stats']:
                agent_stats = game['agent_stats'][agent_name]
                summary['total_moves'] += agent_stats['moves']
                summary['total_nodes'] += agent_stats['total_nodes']
                summary['total_time'] += agent_stats['total_time']
                summary['total_captures'] += agent_stats['captures']
        
        # Calculate averages
        if summary['games_played'] > 0:
            summary['avg_nodes_per_game'] = summary['total_nodes'] / summary['games_played']
            summary['avg_time_per_game'] = summary['total_time'] / summary['games_played']
            summary['win_rate'] = summary['wins'] / summary['games_played'] * 100
        
        return summary
    
    def print_agent_summary(self, agent_name):
        """Print formatted summary for an agent"""
        summary = self.get_agent_summary(agent_name)
        
        print(f"\n{'='*60}")
        print(f"Performance Summary: {agent_name}")
        print(f"{'='*60}")
        print(f"Games Played:        {summary['games_played']}")
        print(f"Wins:                {summary['wins']}")
        print(f"Losses:              {summary['losses']}")
        print(f"Draws:               {summary['draws']}")
        print(f"Win Rate:            {summary['win_rate']:.1f}%")
        print(f"Total Moves:         {summary['total_moves']}")
        print(f"Total Captures:      {summary['total_captures']}")
        print(f"Avg Nodes/Game:      {summary['avg_nodes_per_game']:.0f}")
        print(f"Avg Time/Game:       {summary['avg_time_per_game']:.2f}s")
        print(f"{'='*60}\n")
    
    def compare_agents(self, agent1_name, agent2_name):
        """
        Compare two agents and print statistics
        
        Args:
            agent1_name: Name of first agent
            agent2_name: Name of second agent
        """
        summary1 = self.get_agent_summary(agent1_name)
        summary2 = self.get_agent_summary(agent2_name)
        
        print(f"\n{'='*80}")
        print(f"Agent Comparison: {agent1_name} vs {agent2_name}")
        print(f"{'='*80}")
        print(f"{'Metric':<25} {agent1_name:<25} {agent2_name:<25}")
        print("-" * 80)
        
        metrics = [
            ('Games Played', 'games_played'),
            ('Wins', 'wins'),
            ('Win Rate', 'win_rate', '%'),
            ('Avg Nodes/Game', 'avg_nodes_per_game', ''),
            ('Avg Time/Game', 'avg_time_per_game', 's'),
        ]
        
        for metric_name, metric_key, *unit in metrics:
            unit_str = unit[0] if unit else ''
            val1 = summary1[metric_key]
            val2 = summary2[metric_key]
            
            if isinstance(val1, float):
                print(f"{metric_name:<25} {val1:<24.2f}{unit_str} {val2:<24.2f}{unit_str}")
            else:
                print(f"{metric_name:<25} {val1:<25} {val2:<25}")
        
        print(f"{'='*80}\n")


class MoveQualityAnalyzer:
    """
    Analyzer for evaluating move quality
    """
    
    @staticmethod
    def analyze_move_quality(move_data, board_before, board_after):
        """
        Analyze the quality of a move
        
        Args:
            move_data: Move data dictionary
            board_before: Board state before move
            board_after: Board state after move
        
        Returns:
            Dictionary with quality metrics
        """
        quality = {
            'material_change': 0,
            'position_improvement': 0,
            'tactical_value': 0,
            'overall_score': 0,
        }
        
        # Material change
        if board_before and board_after:
            material_before = (board_before.red_left + 2 * board_before.red_kings) - \
                             (board_before.white_left + 2 * board_before.white_kings)
            material_after = (board_after.red_left + 2 * board_after.red_kings) - \
                            (board_after.white_left + 2 * board_after.white_kings)
            
            quality['material_change'] = abs(material_after - material_before)
        
        # Tactical value (captures are good)
        if move_data.get('was_capture', False):
            quality['tactical_value'] = 10
        
        # Overall score
        quality['overall_score'] = quality['material_change'] * 5 + quality['tactical_value']
        
        return quality


# Global logger instance
performance_logger = PerformanceLogger()


def log_game_start(agent1_name, agent2_name):
    """Convenience function to start logging a game"""
    performance_logger.start_game(agent1_name, agent2_name)


def log_move(agent_name, color, move_number, move_info, **kwargs):
    """Convenience function to log a move"""
    performance_logger.log_move(agent_name, color, move_number, move_info, **kwargs)


def log_game_end(winner_name=None, reason='normal'):
    """Convenience function to end logging a game"""
    performance_logger.end_game(winner_name, reason)
