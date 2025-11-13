import { BaseCard } from '#components/cards';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('BaseCard', () => {
  let component: BaseCard<number>;
  let fixture: ComponentFixture<BaseCard<number>>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BaseCard],
    }).compileComponents();

    fixture = TestBed.createComponent(BaseCard<number>);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
