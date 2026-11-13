#include <string>
#include <vector>
#include "logic.h"
#include "player.h"
#include <fstream>

using std::string, std::vector;

vector<vector<char>> LoadLevel(const string& file, int& h, int& w, Player& p) {
  std::ifstream f{file};
  if (!f) {
    return {};
  }

  long long rows = 0;
  long long cols = 0;
  long long player_row = 0;
  long long player_col = 0;
  constexpr long long INT32_MAX_VALUE = 2147483647LL;

  if (!(f >> rows >> cols >> player_row >> player_col)) {
    return {};
  }
  if (rows <= 0 || cols <= 0 || rows > INT32_MAX_VALUE || cols > INT32_MAX_VALUE ||
    rows > INT32_MAX_VALUE / cols) {
    return {};
  }
  if (player_row < 0 || player_row >= rows ||
    player_col < 0 || player_col >= cols) {
    return {};
  }

  vector<vector<char>> level;
  for (long long r = 0; r < rows; ++r) {
    vector<char> row;
    for (long long c = 0; c < cols; ++c) {
      char tile = 0;
      if (!(f >> tile)) {
        return {};
      }

      if (tile != TILE_OPEN && tile != TILE_TREASURE && tile != TILE_AMULET &&
        tile != TILE_MONSTER && tile != TILE_PILLAR && tile != TILE_DOOR &&
        tile != TILE_EXIT && tile != '|') {
        return {};
      }
      row.push_back(tile);
    }
    level.push_back(row);
  }

  char extra = 0;
  if (f >> extra || f.bad()) {
    return {};
  }

  const int loaded_rows = static_cast<int>(rows);
  const int loaded_cols = static_cast<int>(cols);
  const int loaded_player_row = static_cast<int>(player_row);
  const int loaded_player_col = static_cast<int>(player_col);
  if (level[loaded_player_row][loaded_player_col] == TILE_PILLAR ||
    level[loaded_player_row][loaded_player_col] == TILE_MONSTER) {
    return {};
  }

  level[loaded_player_row][loaded_player_col] = TILE_PLAYER;
  h = loaded_rows;
  w = loaded_cols;
  p.row = loaded_player_row;
  p.col = loaded_player_col;
  return level;
}

void GetDirection(char c, int& y, int& x) {
  // TODO(student): implement this function
  switch(c){
    case 'w':
      y -= 1;
      break;
    case 'a':
      x -= 1;
      break;
    case 's':
      y += 1;
      break;
    case 'd':
      x += 1;
      break;
    default:
      break;
    }
}

void ResizeMap(vector<vector<char>>& map, int& max_row, int& max_col) {
  constexpr long long INT32_MAX_VALUE = 2147483647LL;

  if (max_row <= 0 || max_col <= 0) {
    return;
  }

  const long long new_row_count = 2LL * max_row;
  const long long new_col_count = 2LL * max_col;
  if (new_row_count > INT32_MAX_VALUE || new_col_count > INT32_MAX_VALUE ||
      new_row_count > INT32_MAX_VALUE / new_col_count) {
    return;
  }

  if (map.size() != static_cast<vector<vector<char>>::size_type>(max_row)) {
    return;
  }
  for (const auto& row : map) {
    if (row.size() != static_cast<vector<char>::size_type>(max_col)) {
      return;
    }
  }

  int old_row = max_row;
  int old_col = max_col;

  vector<vector<char>> new_map(
    2 * old_row,
    vector<char>(2 * old_col, TILE_OPEN)
  );

  for (int r = 0; r < old_row; ++r) {
    for (int c = 0; c < old_col; ++c) {
      char tile = map[r][c];

      if (tile == TILE_PLAYER) {
        // keep the original player only in the top-left
        new_map[r][c] = TILE_PLAYER;
        continue;
      }

      new_map[r][c] = tile;
      new_map[r][c + old_col] = tile;
      new_map[r + old_row][c] = tile;
      new_map[r + old_row][c + old_col] = tile;
    }
  }

  map = new_map;
  max_row *= 2;
  max_col *= 2;
}

int DoPlayerMove(vector<vector<char>>& map, int max_row, int max_col,
                 Player& player, int next_row, int next_col) {
  if (abs(next_row - player.row) + abs(next_col - player.col) != 1) {
    return STATUS_STAY;
  }

  if (next_row < 0 || next_row >= max_row ||
      next_col < 0 || next_col >= max_col) {
    return STATUS_STAY;
  }

  char target = map[next_row][next_col];

  if (target == TILE_PILLAR || target == TILE_MONSTER) {
    return STATUS_STAY;
  }

  if (target == TILE_EXIT && player.treasure <= 0) {
    return STATUS_STAY;
  }

  map[player.row][player.col] = TILE_OPEN;
  player.row = next_row;
  player.col = next_col;

  if (target == TILE_TREASURE) {
    player.treasure++;
    map[player.row][player.col] = TILE_PLAYER;
    return STATUS_TREASURE;
  }

  if (target == TILE_AMULET) {
    map[player.row][player.col] = TILE_PLAYER;
    return STATUS_AMULET;
  }

  if (target == TILE_DOOR) {
    map[player.row][player.col] = TILE_PLAYER;
    return STATUS_LEAVE;
  }

  if (target == TILE_EXIT) {
    map[player.row][player.col] = TILE_PLAYER;
    return STATUS_ESCAPE;
  }

  map[player.row][player.col] = TILE_PLAYER;
  return STATUS_MOVE;
}

bool DoMonsterAttack(vector<vector<char>>& map, int max_row, int max_col, const Player& player) {
  bool caught = false;
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};

  for (int dir = 0; dir < 4; ++dir) {
    int r = player.row + dr[dir];
    int c = player.col + dc[dir];
    int toward_row = player.row;
    int toward_col = player.col;

    while (r >= 0 && r < max_row && c >= 0 && c < max_col) {
      char tile = map[r][c];
      if (tile == TILE_PILLAR || tile == '|') {
        break;
      }

      if (tile == TILE_MONSTER) {
        map[r][c] = TILE_OPEN;
        if (toward_row == player.row && toward_col == player.col) {
          map[player.row][player.col] = TILE_MONSTER;
          caught = true;
        } else {
          map[toward_row][toward_col] = TILE_MONSTER;
        }
        break;
      }

      toward_row = r;
      toward_col = c;
      r += dr[dir];
      c += dc[dir];
    }
  }

  return caught;
}