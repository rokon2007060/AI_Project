"""
AI Agent Comparison and Tournament System
Compare different AI agents in head-to-head matches
"""
import time
import sys
from board import Board
from constants import PLAYER1_COLOR, PLAYER2_COLOR
from ai_player import get_best_move
from ai_agents import FuzzyMinimaxAgent, HeuristicBacktrackAgent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_tournament.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AIMatch:
    """
    Represents a single match between two AI agents
    """
    
    def __init__(self, agent1, agent2, agent1_name, agent2_name, max_moves=200):
        """
        Initialize a match
        
        Args:
            agent1: AI agent for PLAYER1 (Red)
            agent2: AI agent for PLAYER2 (White)
            agent1_name: Name of agent 1
            agent2_name: Name of agent 2
            max_moves: Maximum moves before declaring draw
        """
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent1_name = agent1_name
        self.agent2_name = agent2_name
        self.max_moves = max_moves
        self.board = Board()
        self.move_count = 0
        self.winner = None
        self.stats = {
            'agent1': {
                'total_nodes': 0,
                'total_time': 0,
                'moves': 0,
                'captures': 0,
            },
            'agent2': {
                'total_nodes': 0,
                'total_time': 0,
                'moves': 0,
                'captures': 0,
            }
        }
    
    def play_game(self):
        """
        Play a complete game between the two agents
        
        Returns:
            Winner color or None for draw
        """
        logger.info(f"Starting match: {self.agent1_name} (Red) vs {self.agent2_name} (White)")
        
        current_turn = PLAYER1_COLOR
        
        while self.move_count < self.max_moves:
            self.move_count += 1
            
            # Check for winner
            winner = self.board.winner()
            if winner is not None:
                self.winner = winner
                logger.info(f"Game ended! Winner: {self.agent1_name if winner == PLAYER1_COLOR else self.agent2_name}")
                return winner
            
            # Check for no valid moves (stalemate)
            pieces = self.board.get_all_pieces(current_turn)
            has_moves = False
            for piece in pieces:
                if len(self.board.get_valid_moves(piece)) > 0:
                    has_moves = True
                    break
            
            if not has_moves:
                # Player with no moves loses
                self.winner = PLAYER2_COLOR if current_turn == PLAYER1_COLOR else PLAYER1_COLOR
                logger.info(f"Stalemate! Winner: {self.agent1_name if self.winner == PLAYER1_COLOR else self.agent2_name}")
                return self.winner
            
            # Get current agent
            if current_turn == PLAYER1_COLOR:
                current_agent = self.agent1
                agent_name = self.agent1_name
                stats_key = 'agent1'
            else:
                current_agent = self.agent2
                agent_name = self.agent2_name
                stats_key = 'agent2'
            
            # Get move
            start_time = time.time()
            
            if current_agent is None:
                # Original AI
                new_board, move_info, was_capture = get_best_move(self.board, current_turn, depth=3)
                nodes_expanded = 0  # Original AI doesn't track this
            else:
                # New AI agent
                new_board, move_info, was_capture = current_agent.get_move(self.board, None)
                nodes_expanded = current_agent.nodes_expanded if hasattr(current_agent, 'nodes_expanded') else 0
            
            move_time = time.time() - start_time
            
            # Update statistics
            self.stats[stats_key]['total_nodes'] += nodes_expanded
            self.stats[stats_key]['total_time'] += move_time
            self.stats[stats_key]['moves'] += 1
            if was_capture:
                self.stats[stats_key]['captures'] += 1
            
            # Check if move is valid
            if new_board is None:
                logger.warning(f"{agent_name} returned invalid move. Opponent wins.")
                self.winner = PLAYER2_COLOR if current_turn == PLAYER1_COLOR else PLAYER1_COLOR
                return self.winner
            
            # Apply move
            self.board = new_board
            
            # Log move (every 10 moves)
            if self.move_count % 10 == 0:
                logger.info(f"Move {self.move_count}: {agent_name} moved (time: {move_time:.3f}s, nodes: {nodes_expanded})")
            
            # Switch turns
            current_turn = PLAYER2_COLOR if current_turn == PLAYER1_COLOR else PLAYER1_COLOR
        
        # Max moves reached - draw
        logger.info(f"Game ended in draw after {self.max_moves} moves")
        return None
    
    def get_stats_summary(self):
        """Get summary statistics for the match"""
        summary = {
            'winner': 'Draw' if self.winner is None else (self.agent1_name if self.winner == PLAYER1_COLOR else self.agent2_name),
            'total_moves': self.move_count,
        }
        
        for agent_key, agent_name in [('agent1', self.agent1_name), ('agent2', self.agent2_name)]:
            stats = self.stats[agent_key]
            moves = stats['moves']
            
            summary[agent_name] = {
                'total_moves': moves,
                'total_nodes': stats['total_nodes'],
                'total_time': stats['total_time'],
                'captures': stats['captures'],
                'avg_nodes_per_move': stats['total_nodes'] / moves if moves > 0 else 0,
                'avg_time_per_move': stats['total_time'] / moves if moves > 0 else 0,
            }
        
        return summary


class AITournament:
    """
    Tournament system for comparing multiple AI agents
    """
    
    def __init__(self):
        """Initialize tournament"""
        self.agents = {}
        self.results = {}
    
    def register_agent(self, name, agent_class, **kwargs):
        """
        Register an AI agent for the tournament
        
        Args:
            name: Name of the agent
            agent_class: Class of the agent (or None for original AI)
            **kwargs: Arguments to pass to agent constructor
        """
        self.agents[name] = (agent_class, kwargs)
        logger.info(f"Registered agent: {name}")
    
    def run_round_robin(self, games_per_matchup=3):
        """
        Run round-robin tournament where each agent plays each other agent
        
        Args:
            games_per_matchup: Number of games per matchup (alternating colors)
        
        Returns:
            Dictionary of results
        """
        agent_names = list(self.agents.keys())
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting Round-Robin Tournament")
        logger.info(f"Agents: {', '.join(agent_names)}")
        logger.info(f"Games per matchup: {games_per_matchup}")
        logger.info(f"{'='*60}\n")
        
        # Initialize results
        for name in agent_names:
            self.results[name] = {
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'total_nodes': 0,
                'total_time': 0,
                'total_moves': 0,
                'total_captures': 0,
            }
        
        # Play all matchups
        matchup_count = 0
        total_matchups = len(agent_names) * (len(agent_names) - 1) * games_per_matchup // 2
        
        for i, name1 in enumerate(agent_names):
            for name2 in agent_names[i+1:]:
                # Play games alternating colors
                for game_num in range(games_per_matchup):
                    matchup_count += 1
                    logger.info(f"\n--- Matchup {matchup_count}/{total_matchups} ---")
                    
                    # Alternate who plays first
                    if game_num % 2 == 0:
                        agent1_name, agent2_name = name1, name2
                    else:
                        agent1_name, agent2_name = name2, name1
                    
                    # Create agents
                    agent1_class, agent1_kwargs = self.agents[agent1_name]
                    agent2_class, agent2_kwargs = self.agents[agent2_name]
                    
                    agent1 = agent1_class(PLAYER1_COLOR, **agent1_kwargs) if agent1_class else None
                    agent2 = agent2_class(PLAYER2_COLOR, **agent2_kwargs) if agent2_class else None
                    
                    # Play match
                    match = AIMatch(agent1, agent2, agent1_name, agent2_name)
                    winner = match.play_game()
                    
                    # Update results
                    stats = match.get_stats_summary()
                    
                    if winner == PLAYER1_COLOR:
                        self.results[agent1_name]['wins'] += 1
                        self.results[agent2_name]['losses'] += 1
                    elif winner == PLAYER2_COLOR:
                        self.results[agent2_name]['wins'] += 1
                        self.results[agent1_name]['losses'] += 1
                    else:
                        self.results[agent1_name]['draws'] += 1
                        self.results[agent2_name]['draws'] += 1
                    
                    # Update statistics
                    for agent_name in [agent1_name, agent2_name]:
                        if agent_name in stats:
                            agent_stats = stats[agent_name]
                            self.results[agent_name]['total_nodes'] += agent_stats['total_nodes']
                            self.results[agent_name]['total_time'] += agent_stats['total_time']
                            self.results[agent_name]['total_moves'] += agent_stats['total_moves']
                            self.results[agent_name]['total_captures'] += agent_stats['captures']
                    
                    # Log match summary
                    logger.info(f"Match result: {stats['winner']}")
                    logger.info(f"Total moves: {stats['total_moves']}")
        
        return self.results
    
    def print_tournament_results(self):
        """Print formatted tournament results"""
        logger.info(f"\n{'='*80}")
        logger.info("TOURNAMENT RESULTS")
        logger.info(f"{'='*80}\n")
        
        # Sort by wins
        sorted_agents = sorted(self.results.items(), key=lambda x: (x[1]['wins'], -x[1]['losses']), reverse=True)
        
        # Print header
        logger.info(f"{'Rank':<6} {'Agent':<25} {'Wins':<6} {'Losses':<8} {'Draws':<6} {'Win%':<8} {'Avg Time':<10} {'Avg Nodes':<12}")
        logger.info("-" * 80)
        
        # Print results
        for rank, (name, stats) in enumerate(sorted_agents, 1):
            total_games = stats['wins'] + stats['losses'] + stats['draws']
            win_rate = (stats['wins'] / total_games * 100) if total_games > 0 else 0
            avg_time = stats['total_time'] / stats['total_moves'] if stats['total_moves'] > 0 else 0
            avg_nodes = stats['total_nodes'] / stats['total_moves'] if stats['total_moves'] > 0 else 0
            
            logger.info(f"{rank:<6} {name:<25} {stats['wins']:<6} {stats['losses']:<8} {stats['draws']:<6} "
                       f"{win_rate:<7.1f}% {avg_time:<9.3f}s {avg_nodes:<12.0f}")
        
        logger.info(f"\n{'='*80}\n")


def main():
    """Run a sample tournament"""
    tournament = AITournament()
    
    # Register agents
    tournament.register_agent("Original AI", None)  # Original minimax AI
    tournament.register_agent("Fuzzy Minimax", FuzzyMinimaxAgent, depth=4)
    tournament.register_agent("Heuristic CSP", HeuristicBacktrackAgent, depth=3)
    
    # Run tournament
    results = tournament.run_round_robin(games_per_matchup=2)
    
    # Print results
    tournament.print_tournament_results()
    
    logger.info("Tournament completed. Results saved to ai_tournament.log")


if __name__ == '__main__':
    main()
