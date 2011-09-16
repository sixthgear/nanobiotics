import pstats
p = pstats.Stats('run_game.log-cprofile')
# p.strip_dirs().sort_stats(-1).print_stats()
# p.sort_stats('name')
# p.print_stats()
p.sort_stats('cumulative').print_stats(10)
print '---'
p.sort_stats('time').print_stats(10)
