"""
Complete Tetris Game Implementation
A fully functional Tetris game using Pygame with all standard features.
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# Window dimensions
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + GRID_X_OFFSET * 2 + 200  # Extra space for UI
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + GRID_Y_OFFSET * 2

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)      # I-piece
YELLOW = (255, 255, 0)    # O-piece
PURPLE = (128, 0, 128)    # T-piece
GREEN = (0, 255, 0)       # S-piece
RED = (255, 0, 0)         # Z-piece
BLUE = (0, 0, 255)        # J-piece
ORANGE = (255, 165, 0)    # L-piece

# Game settings
FPS = 60
FALL_SPEED = 0.5  # Seconds per cell
FAST_FALL_SPEED = 0.05
SCORE_PER_LINE = 100
SCORE_MULTIPLIER = {1: 1, 2: 3, 3: 5, 4: 8}  # Bonus for multiple lines

# Tetromino shapes (relative coordinates)
SHAPES = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ],
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)]
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)]
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ]
}

# Color mapping for each piece type
PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}


class Tetromino:
    """Represents a Tetris piece (tetromino)"""
    
    def __init__(self, shape_type, x=GRID_WIDTH // 2 - 1, y=0):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.shape = SHAPES[shape_type]
        self.color = PIECE_COLORS[shape_type]
    
    def get_cells(self):
        """Get the absolute coordinates of all cells in the current piece"""
        cells = []
        for dx, dy in self.shape[self.rotation]:
            cells.append((self.x + dx, self.y + dy))
        return cells
    
    def rotate(self):
        """Rotate the piece clockwise"""
        self.rotation = (self.rotation + 1) % 4
    
    def get_rotated_cells(self):
        """Get cells if rotated (for collision checking)"""
        next_rotation = (self.rotation + 1) % 4
        cells = []
        for dx, dy in self.shape[next_rotation]:
            cells.append((self.x + dx, self.y + dy))
        return cells


class TetrisGame:
    """Main game class handling all game logic"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        
        # Game state
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_timer = 0
        self.fall_speed = FALL_SPEED
        
        # Initialize first pieces
        self.spawn_piece()
        self.next_piece = self.create_random_piece()
    
    def create_random_piece(self):
        """Create a random tetromino"""
        shape_type = random.choice(list(SHAPES.keys()))
        return Tetromino(shape_type)
    
    def spawn_piece(self):
        """Spawn a new piece at the top"""
        if self.next_piece:
            self.current_piece = self.next_piece
            self.current_piece.x = GRID_WIDTH // 2 - 1
            self.current_piece.y = 0
        else:
            self.current_piece = self.create_random_piece()
        
        self.next_piece = self.create_random_piece()
        
        # Check for game over
        if self.check_collision(self.current_piece):
            self.game_over = True
    
    def check_collision(self, piece, dx=0, dy=0):
        """Check if piece collides with walls or other pieces"""
        cells = piece.get_cells()
        for x, y in cells:
            new_x, new_y = x + dx, y + dy
            
            # Check walls
            if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                return True
            
            # Check other pieces (only check if below top)
            if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                return True
        
        return False
    
    def check_rotation_collision(self, piece):
        """Check if rotation would cause collision"""
        cells = piece.get_rotated_cells()
        for x, y in cells:
            # Check walls
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return True
            
            # Check other pieces
            if y >= 0 and self.grid[y][x] != BLACK:
                return True
        
        return False
    
    def lock_piece(self):
        """Lock the current piece into the grid"""
        cells = self.current_piece.get_cells()
        for x, y in cells:
            if y >= 0:  # Only lock if piece is on the grid
                self.grid[y][x] = self.current_piece.color
        
        # Check for full lines
        self.clear_lines()
        
        # Spawn next piece
        self.spawn_piece()
    
    def clear_lines(self):
        """Clear full horizontal lines and update score"""
        lines_to_clear = []
        
        # Find full lines (check from bottom to top for proper indexing)
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # If no lines to clear, return early
        if not lines_to_clear:
            return
        
        # Build new grid without full rows
        # Keep only rows that are not full
        new_grid = []
        for y in range(GRID_HEIGHT):
            if y not in lines_to_clear:
                new_grid.append(self.grid[y])
        
        # Add empty rows at the top to maintain grid height
        num_cleared = len(lines_to_clear)
        for _ in range(num_cleared):
            new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        # Replace the grid
        self.grid = new_grid
        
        # Update score
        num_lines = num_cleared
        self.lines_cleared += num_lines
        multiplier = SCORE_MULTIPLIER.get(num_lines, num_lines * 2)
        self.score += SCORE_PER_LINE * multiplier * self.level
        
        # Level up every 10 lines
        self.level = (self.lines_cleared // 10) + 1
        self.fall_speed = max(0.05, FALL_SPEED - (self.level - 1) * 0.05)
    
    def move_piece(self, dx, dy):
        """Move the current piece"""
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self):
        """Rotate the current piece"""
        if not self.check_rotation_collision(self.current_piece):
            self.current_piece.rotate()
        else:
            # Try wall kicks (shift left/right if rotation hits wall)
            for dx in [-1, 1, -2, 2]:
                self.current_piece.x += dx
                if not self.check_rotation_collision(self.current_piece):
                    self.current_piece.rotate()
                    return
                self.current_piece.x -= dx  # Revert if wall kick doesn't work
    
    def update(self, dt):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Update fall timer
        self.fall_timer += dt
        
        # Check if piece should fall
        if self.fall_timer >= self.fall_speed:
            self.fall_timer = 0
            if not self.move_piece(0, 1):
                self.lock_piece()
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        if self.game_over:
            return
        
        # Pause toggle
        if keys[pygame.K_p]:
            self.paused = not self.paused
        
        if self.paused:
            return
        
        # Movement
        if keys[pygame.K_LEFT]:
            self.move_piece(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move_piece(1, 0)
        if keys[pygame.K_DOWN]:
            if self.move_piece(0, 1):
                self.fall_timer = 0  # Reset timer for faster fall
        
        # Rotation
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.rotate_piece()
    
    def draw_grid(self):
        """Draw the game grid"""
        # Draw grid background
        grid_rect = pygame.Rect(
            GRID_X_OFFSET,
            GRID_Y_OFFSET,
            GRID_WIDTH * CELL_SIZE,
            GRID_HEIGHT * CELL_SIZE
        )
        pygame.draw.rect(self.screen, BLACK, grid_rect)
        
        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            start_pos = (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET)
            end_pos = (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE)
            pygame.draw.line(self.screen, GRAY, start_pos, end_pos, 1)
        
        for y in range(GRID_HEIGHT + 1):
            start_pos = (GRID_X_OFFSET, GRID_Y_OFFSET + y * CELL_SIZE)
            end_pos = (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, GRID_Y_OFFSET + y * CELL_SIZE)
            pygame.draw.line(self.screen, GRAY, start_pos, end_pos, 1)
        
        # Draw locked pieces
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != BLACK:
                    rect = pygame.Rect(
                        GRID_X_OFFSET + x * CELL_SIZE + 1,
                        GRID_Y_OFFSET + y * CELL_SIZE + 1,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
    
    def draw_piece(self, piece, offset_x=0, offset_y=0, preview=False):
        """Draw a tetromino piece"""
        cells = piece.get_cells()
        for x, y in cells:
            # Calculate screen position
            screen_x = GRID_X_OFFSET + (x + offset_x) * CELL_SIZE + 1
            screen_y = GRID_Y_OFFSET + (y + offset_y) * CELL_SIZE + 1
            
            # Only draw if on screen
            if 0 <= y < GRID_HEIGHT:
                rect = pygame.Rect(screen_x, screen_y, CELL_SIZE - 2, CELL_SIZE - 2)
                color = piece.color
                if preview:
                    # Make preview slightly transparent
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 2)
                else:
                    pygame.draw.rect(self.screen, color, rect)
    
    def draw_next_piece(self):
        """Draw the next piece preview in its own dedicated area"""
        if not self.next_piece:
            return
        
        preview_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        preview_y = GRID_Y_OFFSET + 250  # Positioned well below level text and score panel
        
        # Draw preview box background
        box_width = 140
        box_height = 120
        box_rect = pygame.Rect(preview_x - 10, preview_y - 50, box_width, box_height)
        pygame.draw.rect(self.screen, (40, 40, 40), box_rect)  # Dark gray background
        pygame.draw.rect(self.screen, WHITE, box_rect, 2)  # White border
        
        # Draw "Next:" label above the box
        label = self.font.render("Next:", True, WHITE)
        label_y = preview_y - 80
        self.screen.blit(label, (preview_x, label_y))
        
        # Calculate piece bounds for centering
        preview_cells = self.next_piece.shape[0]
        if not preview_cells:
            return
        
        min_x = min(x for x, y in preview_cells)
        max_x = max(x for x, y in preview_cells)
        min_y = min(y for x, y in preview_cells)
        max_y = max(y for x, y in preview_cells)
        
        # Calculate center of the piece shape
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0
        
        # Center the piece in the preview box
        box_center_x = preview_x + box_width // 2 - CELL_SIZE // 2
        box_center_y = preview_y + 10
        
        # Draw each cell of the next piece
        for dx, dy in preview_cells:
            # Calculate position relative to center
            cell_x = box_center_x + (dx - center_x) * CELL_SIZE
            cell_y = box_center_y + (dy - center_y) * CELL_SIZE
            
            # Ensure piece stays within preview box bounds
            if (preview_x - 10 <= cell_x <= preview_x - 10 + box_width and
                preview_y - 50 <= cell_y <= preview_y - 50 + box_height):
                rect = pygame.Rect(cell_x + 1, cell_y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                pygame.draw.rect(self.screen, self.next_piece.color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)
    
    def draw_game_over_screen(self):
        """Draw game over overlay with semi-transparent background and centered panel"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over panel background
        panel_width = 450
        panel_height = 320
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 3)
        
        # Draw "GAME OVER" title
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        title_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 70))
        self.screen.blit(game_over_text, title_rect)
        
        # Draw final score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 140))
        self.screen.blit(score_text, score_rect)
        
        # Draw level reached
        level_text = self.font.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 180))
        self.screen.blit(level_text, level_rect)
        
        # Draw instructions with larger, colored fonts
        restart_text = self.large_font.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 230))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.large_font.render("Press Q to Quit", True, RED)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 280))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_ui(self):
        """Draw UI elements (score, level, etc.) with proper spacing"""
        ui_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        ui_y = GRID_Y_OFFSET
        
        # Draw UI panel background for score/level section
        panel_width = 180
        panel_height = 110
        panel_rect = pygame.Rect(ui_x - 10, ui_y - 10, panel_width, panel_height)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)  # Dark gray background
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)  # White border
        
        # Score (at top of UI panel)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (ui_x, ui_y))
        
        # Level (clearly separated below score)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (ui_x, ui_y + 40))
        
        # Lines cleared (below level, before next piece area)
        lines_text = self.small_font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (ui_x, ui_y + 80))
        
        # Draw next piece preview (positioned well below level text)
        self.draw_next_piece()
        
        # Pause message with overlay
        if self.paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.large_font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        # Game over screen (drawn last to be on top)
        if self.game_over:
            self.draw_game_over_screen()
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        self.draw_grid()
        
        if self.current_piece and not self.game_over:
            self.draw_piece(self.current_piece)
        
        self.draw_ui()
        pygame.display.flip()
    
    def reset(self):
        """Reset the game"""
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_timer = 0
        self.fall_speed = FALL_SPEED
        self.spawn_piece()
        self.next_piece = self.create_random_piece()
    
    def run(self):
        """Main game loop"""
        running = True
        last_rotate_key = False
        last_pause_key = False
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()
                    elif event.key == pygame.K_q:
                        running = False
            
            # Get current key states
            keys = pygame.key.get_pressed()
            
            # Create input dict for handle_input
            # For rotation and pause, only trigger on key press (not hold)
            rotate_pressed = (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not last_rotate_key
            pause_pressed = keys[pygame.K_p] and not last_pause_key
            
            input_keys = {
                pygame.K_LEFT: keys[pygame.K_LEFT],
                pygame.K_RIGHT: keys[pygame.K_RIGHT],
                pygame.K_DOWN: keys[pygame.K_DOWN],
                pygame.K_UP: rotate_pressed,
                pygame.K_SPACE: rotate_pressed,
                pygame.K_p: pause_pressed
            }
            
            self.handle_input(input_keys)
            
            # Update last key states
            last_rotate_key = keys[pygame.K_UP] or keys[pygame.K_SPACE]
            last_pause_key = keys[pygame.K_p]
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = TetrisGame()
    game.run()


if __name__ == "__main__":
    main()

