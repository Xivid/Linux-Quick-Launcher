#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "functions.cpp"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->searcher = new Searcher();

    this->sum = 0;
    this->result.clear();

    ui->listWidget->clear();
    ui->listWidget->hide();

    this->setGeometry(100, 50, 256, 27);
    this->setFixedSize(QSize(256, 27));
    this->setWindowFlags(Qt::FramelessWindowHint);

    ui->lineEdit->setFocusPolicy(Qt::StrongFocus);
    ui->listWidget->setFocusPolicy(Qt::StrongFocus);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::reset()
{
    ui->lineEdit->setText("");
    this->sum = 0;
    this->result.clear();
    ui->listWidget->clear();
    ui->listWidget->hide();
    this->setFixedSize(QSize(256, 27));
    QToolTip::hideText();
}

void MainWindow::run(int index)
{
    QProcess *poc = new QProcess;
    poc->start((this->result[index])[1]);
    reset();
}

void MainWindow::on_lineEdit_textChanged(const QString &keyword)
{
    if (keyword == ":q")
        this->close();

    this->searcher->getlist(this->result, keyword);
    this->sum = this->result.size();

    if (keyword != "" && this->sum != 0)
    {
        ui->listWidget->clear();

        for (int i = 0; i < this->sum; i++)
        {
            QListWidgetItem *item = new QListWidgetItem((this->result[i])[0], ui->listWidget);
            item->setToolTip(this->result[i][2]);
            ui->listWidget->insertItem(i, item);
        }

        ui->listWidget->setFixedSize(QSize(256,  int(20 * (this->sum > 20? 20 : this->sum))));
        this->setFixedSize(QSize(256, 27 + int(19.2 * (this->sum > 20? 20 : this->sum))));
        ui->listWidget->show();
    }
    else
    {
        this->result.clear();
        this->sum = 0;
        ui->listWidget->clear();
        ui->listWidget->hide();
        this->setFixedSize(QSize(256, 27));
    }
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    if (ui->listWidget->hasFocus() && event->key() == Qt::Key_Up && ui->listWidget->currentRow() == 0)
        ui->lineEdit->setFocus();
}

void MainWindow::keyReleaseEvent(QKeyEvent *event)
{
    if (ui->lineEdit->hasFocus())
    {
        switch (event->key())
        {
        case Qt::Key_Return:
            if (this->sum)
                run(0);
            break;
        case Qt::Key_Escape:
            reset();
            break;
        case Qt::Key_Down:
            if (this->sum)
            {
                ui->listWidget->setFocus();
                ui->listWidget->setCurrentRow(0);
            }
            break;
        default:
            break;
        }
    }
    else if (ui->listWidget->hasFocus())
    {
        switch (event->key())
        {
        case Qt::Key_Return:
            run(ui->listWidget->currentRow());
            break;
        case Qt::Key_Escape:
            reset();
            break;
        }
    }
}

void MainWindow::on_listWidget_itemClicked()
{
    run(ui->listWidget->currentRow());
}
