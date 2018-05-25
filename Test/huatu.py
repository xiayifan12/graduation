import matplotlib as mpl
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x_qoe = [4.748, 4.820, 4.837, 4.848, 4.793, 4.823, 4.848, 4.840, 4.831, 4.842]
    x_dj = [4.678, 4.695, 4.509, 4.848, 4.790, 4.695, 4.785, 4.504, 4.822, 4.774]
    plt.xlabel('experiment times')
    plt.ylabel('QoE level')
    plt.plot(x_qoe, color='green', label='QoE optimization algorithm ')
    plt.plot(x_dj, color='red', label='Dijkstra algorithm', linewidth=1, linestyle='-.')
    plt.legend()  # 显示图例
    plt.ylim(4, 5)
    plt.show()
